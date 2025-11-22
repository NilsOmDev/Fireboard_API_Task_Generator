import streamlit as st
import pandas as pd

from Dialog_Manager import standard_zurücksetzen
from Task_Manager import tasks_pool, import_tasks, save_tasks, save_standard_tasks

st.set_page_config(page_title="Einstellungen - Einsatz Pool", layout="wide")

st.page_link("pages/settings.py", label="Einstellungen", icon="⚙️")

st.header("Einsatzszenarien Pool")

st.write("Hier können die Einsatzszenarien angelegt und bearbeitet werden. Neben dem Stichwort und der Beschreibung kann ein Level angegeben werden, um die Häufigkeit zu kennzeichnen. Dabei gilt je höher die Zahl, umso größer die Chance das dieser Einsatz ausgewählt wird.")

import_tasks()
edit_table = st.data_editor(pd.DataFrame(tasks_pool), use_container_width=True, num_rows="dynamic", key="tasks_pool")

btn_left, btn_middle, btn_right = st.columns(3)

if btn_left.button("Liste auf Standard zurücksetzen"):
    standard_zurücksetzen()

if "standard_reset" in st.session_state:
    save_standard_tasks()
    st.success("Liste wurde zurückgesetzt")
    del st.session_state["standard_reset"]

if btn_middle.button("Neu laden"):
    st.rerun()

if btn_right.button("Änderungen speichern"):
    if save_tasks(edit_table):
        st.success("Änderungen gespeichert")
    else:
        st.error("Änderungen konnten nicht gespeichert werden")


