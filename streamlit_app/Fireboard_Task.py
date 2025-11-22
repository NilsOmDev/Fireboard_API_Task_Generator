import random
import time
from pyodide.http import pyfetch
import xml.etree.ElementTree as ET
import io
from global_func import log

import global_vars

#geolocator = Nominatim(user_agent="Fireboard_Task_Generator", scheme="http")

env_tag = 'FIREBOARD_API'

# def set_auth_key(auth_key):
#     subprocess.run(['setx', env_tag, auth_key])
#     os.environ[env_tag] = auth_key

# def get_auth_key():
#     if auth_key := os.environ.get(env_tag):
#         return auth_key
#     log("[ERROR]: Auth-Key for Fireboard Portal is not found. Insert in Systemvariables.")
#     st.warning("Auth-Key for Fireboard Portal is not found.")
#     return "None"

# def replace_umlauts(text):
#     umlaut_map = {
#         "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
#         "Ä": "Ae", "Ö": "Oe", "Ü": "Ue"
#     }
#     for umlaut, replacement in umlaut_map.items():
#         log(text)
#         text = text.replace(umlaut, replacement)
#     return text
    
class FireboardTask:    

    def __init__(self, task, description, number):
        self._task = task
        self._ls_num = "OF" + str(number).zfill(5)
        self._description = description

        self._uni_id = self._generate_unique_id()
        self._time = self._generate_timestamp()
        self._lat, self._long = "53.516", "7.27572"


    async def send_task_to_api(self):
        try:
            self._lat, self._long = await self._geocode_address()
            self._xml_string = self._generate_xml()

            if self._xml_string == "":
                raise Exception("There is no xml_string to send")
            
            url = f"https://login.fireboard.net/api?authkey={global_vars.auth_key}&call=operation_data"
            headers = {'Content-Tpe': 'application/xml'}

            response = await pyfetch(url, method="POST", body=self._xml_string, headers=headers)
        
            log("An Fireboard Portal übertragen...")
            print(await response.text())
            return response
        
        except Exception as e:
            log("[ERROR]: send_task_to_api -> " + str(e))
           
    async def _geocode_address(self):
        try:
            ## TODO: fetch failed ??
            url = f"https://nominatim.openstreetmap.org/search?q={self._task.get_address()}&format=json"
            response = await pyfetch(url, method="GET")
            data = await response.json()
        
            if data:
                return str(data[0]["lat"]), str(data[0]["lon"])
            else:
                log("[ERROR]: Couldn't find a coordinate")

        except Exception as e:
            log("[ERROR]: Couldn't find a coordinate: " + str(e))

        return "53.516", "7.27572"
       
    def _generate_unique_id(self):
        hex_digits = '0123456789ABCDEF'
        unique_digits = [random.choice(hex_digits) for _ in range(20)]

        return ''.join(unique_digits)

    
    def _generate_timestamp(self):
        unix_time = int(time.time())
        timestamp = str(unix_time * 1000)

        return timestamp
    
    def _generate_xml(self):
        root = ET.Element('fireboardOperation')
        root.set('version', '1.0.3')

        uniqueId = ET.SubElement(root, 'uniqueId')
        uniqueId.text = self._uni_id
        basicData = ET.SubElement(root, 'basicData')

        externalNumber = ET.SubElement(basicData, 'externalNumber')
        externalNumber.text = self._ls_num

        keyword = ET.SubElement(basicData, 'keyword')
        keyword.text = self._task.get_message_short()

        announcement = ET.SubElement(basicData, 'announcement')
        announcement.text = self._task.get_message_text()

        location = ET.SubElement(basicData, 'location')
        location.text = self._task.get_address()

        geo_location = ET.SubElement(basicData, 'geo_location')

        latitude = ET.SubElement(geo_location, 'latitude')
        latitude.text = self._lat

        longitude = ET.SubElement(geo_location, 'longitude')
        longitude.text = self._long

        timestampStarted = ET.SubElement(basicData, 'timestampStarted')

        long = ET.SubElement(timestampStarted, 'long')
        long.text = self._time

        situation = ET.SubElement(basicData, 'situation')
        situation.text = self._description
    
        xml_bytes = io.BytesIO()
        tree = ET.ElementTree(root)
        tree.write(xml_bytes, encoding='utf-8', xml_declaration=False)
        xml_string = xml_bytes.getvalue().decode('utf-8')
        
        if global_vars.debug_mode:
            log("XML-String: " + xml_string)
        
        return xml_string