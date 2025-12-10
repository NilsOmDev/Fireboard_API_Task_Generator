import csv
import random
import pandas as pd
import os

from backend.global_func import log

streets_pool = []
tasks_pool = []
cars_pool = []

home_dir = os.path.expanduser("~")
data_dir = home_dir + "/FireboardTaskGenerator/"

streets_pool_csv_name = data_dir + "Streets_Pool.csv"
streets_row_ort_name = "Ort"
streets_row_strasse_name = "Straße"

tasks_pool_csv_name = data_dir + "Tasks_Pool.csv"
tasks_row_stichwort_name = "Stichwort"
tasks_row_stichwort_text_name = "Stichwort Text"
tasks_row_beschreibung_name = "Beschreibung"
tasks_row_level_name = "Häufigkeit"

car_pool_csv_name = data_dir + "Car_Pool.csv"
car_pool_rufname_name = "Rufname"


def import_streets():
    streets_pool.clear()

    if not os.path.exists(streets_pool_csv_name):
        save_standard_streets()

    with open(streets_pool_csv_name, 'r', encoding='utf-8-sig') as csv_file:  
        csv_reader = list(csv.DictReader(csv_file, delimiter=';'))  

        for row in csv_reader:
            streets_pool.append({
                streets_row_ort_name: row.get(streets_row_ort_name, ""),
                streets_row_strasse_name: row.get(streets_row_strasse_name, ""),
            })

def import_tasks():
    tasks_pool.clear()

    if not os.path.exists(tasks_pool_csv_name):
        save_standard_tasks()

    with open(tasks_pool_csv_name, 'r', encoding='utf-8-sig') as csv_file:  
        csv_reader = list(csv.DictReader(csv_file, delimiter=';'))  

        for row in csv_reader:
            tasks_pool.append({
                tasks_row_stichwort_name: row.get(tasks_row_stichwort_name, ""),
                tasks_row_stichwort_text_name: row.get(tasks_row_stichwort_text_name, ""),
                tasks_row_beschreibung_name: row.get(tasks_row_beschreibung_name, ""),
                tasks_row_level_name: row.get(tasks_row_level_name, 0)
            })

def import_cars():
    cars_pool.clear()

    if not os.path.exists(car_pool_csv_name):
        save_standard_cars()

    with open(car_pool_csv_name, 'r', encoding='utf-8-sig') as csv_file:  
        csv_reader = list(csv.DictReader(csv_file, delimiter=';'))  

        for row in csv_reader:
            cars_pool.append({
                car_pool_rufname_name: row.get(car_pool_rufname_name, "")
            })


def save_tasks(edit_table):
    success = True
    with open(tasks_pool_csv_name, 'w', encoding='utf-8', newline='') as csv_file:
        fieldnames = edit_table.columns.tolist()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        csv_writer.writeheader()
        for _, row in edit_table.iterrows():
            if(not(row[tasks_row_stichwort_name]) or 
               not(row[tasks_row_stichwort_text_name]) or 
               not(row[tasks_row_beschreibung_name]) or 
               not(row[tasks_row_level_name]) or
               not(int(row[tasks_row_level_name]) > 0)):
                success = False
                continue
            csv_writer.writerow(row.to_dict())
    
    import_tasks()
    return success

def save_streets(edit_table):
    success = True
    with open(streets_pool_csv_name, 'w', encoding='utf-8-sig', newline='') as csv_file:
        fieldnames = edit_table.columns.tolist()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        csv_writer.writeheader()
        for _, row in edit_table.iterrows():
            if(not(row[streets_row_ort_name]) or 
               not(row[streets_row_strasse_name])):
                success = False
                continue
            csv_writer.writerow(row.to_dict())

    import_streets()
    return success

def save_cars(edit_table):
    success = True
    with open(car_pool_csv_name, 'w', encoding='utf-8-sig', newline='') as csv_file:
        fieldnames = edit_table.columns.tolist()
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        csv_writer.writeheader()
        for _, row in edit_table.iterrows():
            if(not(row[car_pool_rufname_name])):
                success = False
                continue
            csv_writer.writerow(row.to_dict())
    
    import_cars()
    return success

def save_standard_tasks():
    table = [{tasks_row_stichwort_name: 'TH_klein', 
              tasks_row_stichwort_text_name: 'Baum auf Straße', 
              tasks_row_beschreibung_name: 'Baum auf Straße gefallen', 
              tasks_row_level_name: 20}]
    edit_table = pd.DataFrame(table)
    log("[INFO]: Standard Tasks Pool saved")
    save_tasks(edit_table)


def save_standard_streets():
    table = [{streets_row_ort_name: 'Musterstadt', streets_row_strasse_name: 'Musterstraße'}]
    edit_table = pd.DataFrame(table)    
    log("[INFO]: Standard Streets Pool saved")
    save_streets(edit_table)

def save_standard_cars():
    table = [{car_pool_rufname_name: '10-11-2'}]
    edit_table = pd.DataFrame(table)
    log("[INFO]: Standard Cars Pool saved")
    save_cars(edit_table)

def choose_street():
    choosen_street = random.choice(streets_pool)
    # add house number
    address = choosen_street[streets_row_ort_name] + ", " + choosen_street[streets_row_strasse_name] + " " + str(random.randint(1,20))
    return address

#
# Wähle zufällig einen Einsatz aus
# Diese sind dabei gewichtet:
# größeres Level -> größere Häufigkeit
# kleineres Level -> kleinere Häufigkeit
#
def choose_task():

    freq = [row[tasks_row_level_name] for row in tasks_pool]
    weights = [float(i) for i in freq]
    choosen_task = random.choices(tasks_pool, weights=weights)[0]

    msg_short = choosen_task[tasks_row_stichwort_name]
    msg_text = choosen_task[tasks_row_stichwort_text_name]
    description = choosen_task[tasks_row_beschreibung_name]
    
    return msg_short, msg_text, description
    