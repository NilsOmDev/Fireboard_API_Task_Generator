import random
import time
import requests
import xml.etree.ElementTree as ET
import io

from backend.global_func import log
import backend.global_vars as global_vars

env_tag = 'FIREBOARD_API'


class FireboardTask:    

    def __init__(self, task, description, number):
        self._task = task
        self._ls_num = "OF" + str(number).zfill(5)
        self._description = description

        self._uni_id = self._generate_unique_id()
        self._time = self._generate_timestamp()
        self._lat, self._long = "53.516", "7.27572"


    def send_task_to_api(self):
        try:
            self._lat, self._long = self._geocode_address()
            self._xml_string = self._generate_xml()

            if self._xml_string == "":
                raise Exception("There is no xml_string to send")
            
            url = f"https://login.fireboard.net/api?authkey={global_vars.auth_key}&call=operation_data"
            headers = {'Content-Type': 'application/xml'}

            response = requests.post(url, data=self._xml_string, headers=headers)

            log("An Fireboard Portal übertragen...")
            print(response.text)
            return response
        
        except Exception as e:
            log("[ERROR]: send_task_to_api -> " + str(e))


    def _geocode_address(self):
        try:
            query = self._task.get_address()
            url = f"https://nominatim.openstreetmap.org/search"
            params = {"q": query, "format": "json"}

            response = requests.get(url, params=params, timeout=5)
            data = response.json()

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
        return str(unix_time * 1000)
    

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
