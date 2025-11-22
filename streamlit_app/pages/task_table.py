import streamlit as st
from Menu import *
from Dialog_Manager import *
from Dialog_Manager import *
from global_func import log

st.set_page_config(page_title="Einsatzverwaltung", layout="wide")

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
if col1.button("Neuer Einsatz"):
    einsatz_erstellen()

if col2.button("Eigener Einsatz"):
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
