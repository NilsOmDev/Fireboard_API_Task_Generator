import streamlit as st

from backend.Settings_Manager import load_settings
import backend.global_vars as global_vars
from backend.global_func import log

st.set_page_config(page_title="Hauptseite", layout="wide")

log("Starting Fireboard Task Generator ...")

load_settings()

if(global_vars.debug_mode):
    log(st.session_state)

st.header("Menu")
st.page_link("pages/settings.py", label="Einstellungen", icon="⚙️")
st.page_link("pages/task_table.py", label="Einsatzverwaltung", icon="🚨")

