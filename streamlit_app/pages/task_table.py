import streamlit as st
from Menu import *
from Dialog_Manager import *
import asyncio
from datetime import datetime, timedelta
from global_func import log
import random

st.set_page_config(page_title="Einsatzverwaltung", layout="wide")

# ===== Timer Einstellungen =====
if "current_duration" not in st.session_state:
    st.session_state.current_duration = random.randint(global_vars.default_time, global_vars.maximal_time)

if "running" not in st.session_state:
    st.session_state.running = False

if "end_time" not in st.session_state:
    st.session_state.end_time = datetime.now() + timedelta(seconds=st.session_state.current_duration)

if "current_remaining" not in st.session_state:
    st.session_state.current_remaining = st.session_state.current_duration

def status_num_to_icon(status):
    if status == 1:
        return ":one:"
    elif status == 2:
        return ":two:"
    elif status == 3: 
        return ":three:"
    elif status == 4:
        return ":four:"
    else:
        return ":question:"
    

if(global_vars.debug_mode):
    log(st.session_state)

cols = st.columns(4)
cols[0].page_link("streamlit_app.py", label="Menu", icon="🏠")
cols[1].page_link("pages/settings.py", label="Einstellungen", icon="⚙️")

st.header("Einsatzverwaltung")

def reload_table():
    st.rerun()

if "cmd_stack" not in st.session_state:
    st.session_state.cmd_stack = []

# Buttons für Aktionen
col1, col2, col3, col4, col5, col6 = st.columns(6)
if col1.button("Neuer Einsatz", disabled=st.session_state.running):
    einsatz_erstellen()

if col2.button("Eigener Einsatz", disabled=st.session_state.running):
    eigenen_einsatz_erstellen()


        
# if col5.button("Undo"):
#     if st.warning("Letzten Befehl rückgängig machen?"):
#         undo_func()
#         reload_table()

# if col6.button("Beenden"):
#     st.stop()

_table = get_table()
column_cars = _table[0].index("Fahrzeuge") + 1
column_info = _table[0].index("Infos") + 1

for idx_row, row in enumerate(_table):
    cols = st.columns(len(row) + 1)
    
    if idx_row > 0:
        if cols[0].button("X", key=f"btn_{idx_row}_delete", help="Einsatz löschen"):
           einsatz_löschen(idx_row)
    
    for idx_column, value in enumerate(row, 1):
        if idx_row > 0:
            if idx_column == column_cars:
                for car in value:
                    with cols[idx_column]:
                        in_col1, in_col2, in_col3 = st.columns(3)
                        in_col1.write(car[0])                       # Funkrufname
                        in_col2.write(status_num_to_icon(car[1]))      # Status
                        
                        if in_col3.button("", icon="⬆️", key=f"btn_{idx_row}_{idx_column}_{car}", ):
                            change_status_func(idx_row, car[0])
                            reload_table()                       
            elif idx_column == column_info:
                for inner_val in value:
                    cols[idx_column].write(inner_val)
            else:
                cols[idx_column].write(value)

            if idx_column == column_info or idx_column == column_cars:
                if cols[idx_column].button("", icon="➕", key=f"btn_{idx_row}_{idx_column}"):
                    if idx_column == column_cars:
                        fahrzeug_hinzufuegen(idx_row)
                    elif idx_column == column_info:
                        info_hinzufuegen(idx_row)
        else:
            cols[idx_column].write(value)

if "fahrzeug_hinzufuegen" in st.session_state:
    car = st.session_state.fahrzeug_hinzufuegen['car']
    line = st.session_state.fahrzeug_hinzufuegen['idx_row']
    
    if car: 
        del st.session_state["fahrzeug_hinzufuegen"]
        add_car_func(line, car)
        reload_table()

if "info_hinzufuegen" in st.session_state:
    info = st.session_state.info_hinzufuegen['info']
    line = st.session_state.info_hinzufuegen['idx_row']
    
    if info:
        del st.session_state["info_hinzufuegen"]
        add_info_func(line, info)
        reload_table()

if "eigenen_einsatz_erstellen" in st.session_state:
    town = st.session_state.eigenen_einsatz_erstellen['town']
    street = st.session_state.eigenen_einsatz_erstellen['street'] 
    number = st.session_state.eigenen_einsatz_erstellen['number']
    msg_short = st.session_state.eigenen_einsatz_erstellen['msg_short']
    msg_text = st.session_state.eigenen_einsatz_erstellen['msg_text']
    description = st.session_state.eigenen_einsatz_erstellen['description']

    if town and street and number:
        address = f"{town}, {street} {number}"
        del st.session_state["eigenen_einsatz_erstellen"]
        create_task(address, msg_short, msg_text, description)
        reload_table()

if "einsatz_erstellen" in st.session_state:
    if st.session_state.einsatz_erstellen['neuer_einsatz']:
        create_task_from_pool()
        del st.session_state["einsatz_erstellen"]
        reload_table()

if "einsatz_löschen" in st.session_state:
    line = st.session_state.einsatz_löschen['idx_row']

    if st.session_state.einsatz_löschen['einsatz_löschen']:
        close_task(line)
        del st.session_state["einsatz_löschen"]
        reload_table()



# ===== UI Controls =====
col1, col2 = st.columns(2)

button_placeholder = col1.empty()
def toggle_running():
    st.session_state.running = not st.session_state.running
    st.session_state.end_time = datetime.now() + timedelta(seconds=st.session_state.current_remaining)

button_label = "Pause" if st.session_state.running else "Start"
button_placeholder.button(button_label, on_click=toggle_running)

ph = col2.empty()
mm, ss = divmod(int(st.session_state.current_remaining), 60)
ph.metric("Neuer Einsatz in:", f"{mm:02d}:{ss:02d}")

# ===== Funktion, die nach Ablauf ausgeführt wird =====
def on_timer_finish():
    log("[INFO]: Timer elapsed.")
    create_task_from_pool()

# ===== Async Countdown Loop =====
async def countdown():
    while st.session_state.running:
        now = datetime.now()
        st.session_state.current_remaining = (st.session_state.end_time - now).total_seconds()

        if st.session_state.current_remaining <= 0:
            on_timer_finish()
            st.session_state.current_duration = random.randint(global_vars.default_time, global_vars.maximal_time)
            st.session_state.end_time = datetime.now() + timedelta(seconds=st.session_state.current_duration)
            st.rerun() # reload table

        # Update UI
        mm, ss = divmod(int(st.session_state.current_remaining), 60)
        ph.metric("Neuer Einsatz in:", f"{mm:02d}:{ss:02d}")
        await asyncio.sleep(1)

# ===== Start Async Loop =====
asyncio.run(countdown())

