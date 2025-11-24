import global_vars
import json
import os
import streamlit as st

from global_func import log

log("Settings: ")
log(os.getcwd())

file_name = "/mnt/settings.json"

def save_settings():  
    variables_to_save = {"send_task" : st.session_state['send_task'],
                         "debug_mode" : st.session_state['debug_mode'], 
                         "auto_delete" : st.session_state['auto_delete'],
                         "auth_key" : st.session_state['auth_key'],
                         "default_time" : st.session_state['default_time'],
                         "maximal_time" : st.session_state['maximal_time'],} 
    
    global_vars.send_task = st.session_state['send_task']
    global_vars.debug_mode = st.session_state['debug_mode']
    global_vars.auto_delete = st.session_state['auto_delete']
    global_vars.auth_key = st.session_state['auth_key']
    global_vars.default_time = st.session_state['default_time']
    global_vars.maximal_time = st.session_state['maximal_time']

    save_settings_raw(variables_to_save)
    log("[INFO]: Settings saved to file.")

def save_settings_raw(dict):
    with open(file_name, "w") as f:
        json.dump(dict, f)

def save_standard_settings():
    variables_to_save = {"send_task" : True, 
                         "debug_mode" : False,
                         "auto_delete" : False,
                         "auth_key": "0123456",
                         "default_time": 60,
                         "maximal_time": 120}
    save_settings_raw(variables_to_save)
    log("[INFO]: Standard settings saved to file.")
    
def load_settings():
    if not os.path.exists(file_name):
        save_standard_settings()

    try:
        with open(file_name, "r") as f:
            json_data = json.load(f)
            st.session_state['send_task'] = json_data["send_task"]
            st.session_state['debug_mode'] = json_data["debug_mode"]
            st.session_state['auto_delete'] = json_data["auto_delete"]
            st.session_state['auth_key'] = json_data["auth_key"]
            st.session_state['default_time'] = json_data["default_time"]
            st.session_state['maximal_time'] = json_data["maximal_time"]

            global_vars.send_task = st.session_state['send_task']
            global_vars.debug_mode = st.session_state['debug_mode']
            global_vars.auto_delete = st.session_state['auto_delete']
            global_vars.auth_key = st.session_state['auth_key']
            global_vars.default_time = st.session_state['default_time']
            global_vars.maximal_time = st.session_state['maximal_time']
            log("[INFO]: Settings loaded from file.")
    except BaseException as e:
        log("[ERROR]: Loading settings from file not succesfull. Creating a new file now.");
        save_standard_settings()