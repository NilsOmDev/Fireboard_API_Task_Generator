import streamlit as st
import pandas as pd

from Dialog_Manager import standard_zurücksetzen
from Task_Manager import streets_pool, import_streets, save_streets, save_standard_streets

st.set_page_config(page_title="Einstellungen - Adressen Pool", layout="wide")

st.page_link("pages/settings.py", label="Einstellungen", icon="⚙️")

st.header("Adressen Pool")

st.write("Hier können die Adressen angelegt und bearbeitet werden. Es reicht den Ort und die Straße anzugeben. Die Hausnummer wird zufällig beim Erstellen generiert.")

import_streets()
edit_table = st.data_editor(pd.DataFrame(streets_pool), use_container_width=True, num_rows="dynamic", key="streets_pool")

btn_left, btn_middle, btn_right = st.columns(3)

if btn_left.button("Liste auf Standard zurücksetzen"):
    standard_zurücksetzen()

if "standard_reset" in st.session_state:
    save_standard_streets()
    st.success("Liste wurde zurückgesetzt")
    del st.session_state["standard_reset"]

if btn_middle.button("Neu laden"):
    st.rerun()

if btn_right.button("Änderungen speichern"):
    if save_streets(edit_table):
        st.success("Änderungen gespeichert")
    else:
        st.error("Änderungen konnten nicht gespeichert werden")