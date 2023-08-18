#
# author = Nils Ommen
# date = 07.08.2023
# version = 1.0
# application use = fireboard api access
# 
# Fireboard_Task.py

import random
import time
import requests
import xml.etree.ElementTree as ET

from Main import auth_key

class FireboardTask:    

    def __init__(self, task, description, number):
        self._task = task
        self._ls_num = "OF" + str(number).zfill(5)
        self._description = description

        # add missing informations
        self._lat, self._long = self._geocode_address()
        self._uni_id = self._generate_unique_id()
        self._time = self._generate_timestamp()

        self._xml_string = self._generate_xml()

    def send_task_to_api(self):
        if self._xml_string == "":
            raise Exception("There is no xml_string to send")
        
        url = 'https://login.fireboard.net/api'
        headers = {'Content-Tpe': 'application/xml'}
        params = {'authkey': auth_key, 'call' : 'operation_data'}

        response = requests.post(url, data=self._xml_string, headers=headers, params=params)
        print("An Fireboard Portal übertragen...")
        print(response.content)

        return response
           

    def _geocode_address(self):
        url = "https://nominatim.openstreetmap.org/search"

        params = {"q": self._task.get_address(), "format": "json"}

        response = requests.get(url, params=params)
        data = response.json()

        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            return lat, lon
        
        return None

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

        xml_string = ET.tostring(root, encoding='utf-8')
        
        return xml_string.decode('utf-8')