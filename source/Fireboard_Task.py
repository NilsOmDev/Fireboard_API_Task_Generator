#
# author = Nils Ommen
# date = 12.08.2024
# version = 2.0
# application use = fireboard api access
# 
# Fireboard_Task.py

import random
import time
import requests
import xml.etree.ElementTree as ET
from geopy.geocoders import Nominatim
import os
import subprocess

geolocator = Nominatim(user_agent="Fireboard_Task_Generator")

env_tag = 'FIREBOARD_API'

def set_auth_key(auth_key):
    subprocess.run(['setx', env_tag, auth_key])
    os.environ[env_tag] = auth_key

def get_auth_key():
    if auth_key := os.environ.get(env_tag):
        return auth_key
    print("[ERROR]: Auth-Key for Fireboard Portal is not found. Insert in Systemvariables.")
    return "0a0a0"
    
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
        params = {'authkey': get_auth_key(), 'call' : 'operation_data'}

        response = requests.post(url, data=self._xml_string, headers=headers, params=params)
        print("An Fireboard Portal übertragen...")
        print(response.content)

        return response
           
    def _geocode_address(self):
        location = geolocator.geocode(self._task.get_address())
        try:
            lat = location.latitude
            lon = location.longitude
            return str(lat), str(lon)
        except AttributeError as e:
            print("[ERROR]: Couldn't find a coordinate")

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

        xml_string = ET.tostring(root, encoding='utf-8')
       
        return xml_string.decode('utf-8')