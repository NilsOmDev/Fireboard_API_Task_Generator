import streamlit as st 

from Task_Manager import cars_pool

@st.dialog("Fahrzeug hinzufügen")
def fahrzeug_hinzufuegen(idx_row):
    car = st.selectbox("Fahrzeug", [item['Rufname'] for item in cars_pool])
    
    if st.button("Bestätigen"):
        st.session_state.fahrzeug_hinzufuegen = {"car": car, "idx_row": idx_row}   
        st.rerun()

@st.dialog("Info hinzufügen")
def info_hinzufuegen(idx_row):
    info = st.text_input("Info")

    if st.button("Bestätigen"):
        st.session_state.info_hinzufuegen = {"info": info, "idx_row": idx_row}   
        st.rerun()

@st.dialog("Auth-Key setzen")  
def auth_key_setzen():
    auth_key = st.text_input("Auth-Key")

    if st.button("Bestätigen"):
        st.session_state.auth_key_setzen = {"auth_key": auth_key}   
        st.rerun()

@st.dialog("Eigenen Einsatz erstellen")
def eigenen_einsatz_erstellen():

    town = st.text_input("Ort")
    street = st.text_input("Straße")
    number = st.text_input("Hausnummer")
    msg_short = st.text_input("Stichwort")
    msg_text = st.text_input("Stichwort Text")
    description = st.text_input("Beschreibung")

    if st.button("Bestätigen"):
        st.session_state.eigenen_einsatz_erstellen = {"town": town, "street": street, "number": number, "msg_short": msg_short, "msg_text": msg_text, "description": description}   
        st.rerun()

@st.dialog("Einsatz erstellen?")
def einsatz_erstellen():

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ja"):
            st.session_state.einsatz_erstellen = {"neuer_einsatz": True}   
            st.rerun()
    with col2: 
        if st.button("Nein"):
            st.rerun()

@st.dialog("Auf Standard zurücksetzen?")
def standard_zurücksetzen():

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ja"):
            st.session_state.standard_reset = {"standard_reset": True}   
            st.rerun()
    with col2: 
        if st.button("Nein"):
            st.rerun()

@st.dialog("Einsatz löschen?")
def einsatz_löschen(idx_row):

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ja"):
            st.session_state.einsatz_löschen = {"einsatz_löschen": True, "idx_row": idx_row}   
            st.rerun()
    with col2: 
        if st.button("Nein"):
            st.rerun()