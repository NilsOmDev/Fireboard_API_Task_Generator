import streamlit as st
import pandas as pd

from Dialog_Manager import standard_zurücksetzen
from Task_Manager import cars_pool, import_cars, save_cars, save_standard_cars

st.set_page_config(page_title="Einstellungen - Fahrzeug Pool", layout="wide")

st.page_link("pages/settings.py", label="Einstellungen", icon="⚙️")

st.header("Fahrzeug Pool")

import_cars()
edit_table = st.data_editor(pd.DataFrame(cars_pool), use_container_width=True, num_rows="dynamic", key="cars_pool")

btn_left, btn_middle, btn_right = st.columns(3)

if btn_left.button("Liste auf Standard zurücksetzen"):
    standard_zurücksetzen()

if "standard_reset" in st.session_state:
    save_standard_cars()
    st.success("Liste wurde zurückgesetzt")
    del st.session_state["standard_reset"]

if btn_middle.button("Neu laden"):
    st.rerun()

if btn_right.button("Änderungen speichern"):
    if save_cars(edit_table):
        st.success("Änderungen gespeichert")
    else:
        st.error("Änderungen konnten nicht gespeichert werden")