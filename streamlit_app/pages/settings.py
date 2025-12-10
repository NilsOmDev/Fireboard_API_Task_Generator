import streamlit as st

from backend.Settings_Manager import load_settings, save_settings
from backend.global_func import log
import backend.global_vars as global_vars

st.set_page_config(page_title="Einstellungen", layout="wide")

load_settings()

if(global_vars.debug_mode):
    log(st.session_state)

cols = st.columns(4)
cols[0].page_link("streamlit_app.py", label="Menu", icon="🏠")
cols[1].page_link("pages/task_table.py", label="Einsatzverwaltung", icon="🚨")

st.header("Einstellungen")

st.write("Der Auth-Key wird lokal auf diesem Gerät gespeichert. Ist keiner hinterlegt, können keine Daten an das Fireboard Portal gesendet werden. Er ist im Fireboard Portal unter \"Auth-Key Verwaltung\" zu finden. Es wird der Auth-Key für die Alarmdatenübernahme benötigt.")

st.page_link("https://login.fireboard.net/account/authkeys", label = "Fireboard Portal", icon = "🔗")

col_left, col_right = st.columns(2, vertical_alignment="bottom")
st.session_state['auth_key'] = col_left.text_input("Auth-Key", global_vars.auth_key, key="auth_key_input")

if col_right.button("Speichern"):
        save_settings()
        log("[INFO]: Auth-Key gesetzt: " + global_vars.auth_key)


st.divider()

st.write("Hier können die Einsatzsenarien bearbeitet werden:")
st.page_link("pages/settings_tasks_pool.py", label = "Einsatz Pool", icon = "🔥")

st.write("Hier können die Fahrzeuge bearbeitet werden:")
st.page_link("pages/settings_cars_pool.py", label = "Fahrzeug Pool", icon = "🚗")

st.write("Hier können die Adressen bearbeitet werden:")
st.page_link("pages/settings_streets_pool.py", label = "Adressen Pool", icon = "🛣️")

st.divider()

st.write("Aktiviere hier das Senden an die Fireboard API.")
st.session_state['send_task'] = st.toggle("Einsätze an Fireboard API senden?", key="send_task_input", value=global_vars.send_task, on_change=save_settings)

st.divider()

st.write("Sollen Einsätze automatisch gelöscht werden, sobald alle Fahrzeuge den Status 1 erreicht haben?")
st.session_state['auto_delete'] = st.toggle("Automatisches Löschen aktivieren?", key="auto_delete_input", value=st.session_state['auto_delete'], on_change=save_settings)

st.divider()

st.write("Entwickler Einstellung: Debug Mode aktivieren, um mehr Informationen in der Konsole einzustellen. ")
st.session_state['debug_mode'] = st.toggle("Debug Mode", key="debug_mode_input", value=global_vars.debug_mode, on_change=save_settings)

st.divider()

st.write("Timer Einstellungen für automatische Einsatzerstellung.")

st.write("Nach Ablauf einer zufälligen Zeit innerhalb der minimalen bis zur maximalen Zeitdauer, wird ein neuer Einsatz erstellt.")
st.session_state['default_time'] = st.number_input("Minimale Zeitdauer: ", value=st.session_state['default_time'], min_value=1, max_value=st.session_state['maximal_time'], key="default_time_input")
st.session_state['maximal_time'] = st.number_input("Maximale Zeitdauer: ", value=st.session_state['maximal_time'], min_value=st.session_state['default_time'], key="maximal_time_input")

if st.button("Speichern", key="save_time"):
    save_settings()
