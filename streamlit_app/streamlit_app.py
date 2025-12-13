# -*- coding: utf-8 -*-
import os
import sys
import streamlit.components.v1 as components

def init_autorefresh():
    """Initialisiert den Streamlit-Autorefresh-Component sicher unter PyInstaller."""
    # Pfad zu den Component-Assets bestimmen
    if hasattr(sys, '_MEIPASS'):
        # Onefile → Assets sind im _MEIPASS entpackt
        component_root = os.path.join(sys._MEIPASS, "streamlit_autorefresh", "frontend", "build")
    else:
        # Normal oder onedir – Pfad zum installierten Package
        import streamlit_autorefresh
        component_root = os.path.join(os.path.dirname(streamlit_autorefresh.__file__), "frontend", "build")

    # Component registrieren
    return components.declare_component("st_autorefresh", path=component_root)

# GLOBALE FUNKTION exportieren
st_autorefresh = init_autorefresh()

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
