#
# author = Nils Ommen
# date = 07.08.2023
# version = 1.0
# application use = fireboard api access
# 
# Task_Manager.py

import csv
import random

streets_pool = []
tasks_pool = []


def import_streets():
    with open('Streets_Pool.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            streets_pool.append(row)

def import_tasks():
    with open('Tasks_Pool.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for row in csv_reader:
            tasks_pool.append(row)


def choose_street():
    choosen_street = random.choice(streets_pool)
    # add house number
    address = choosen_street['Ort, Strasse'] + " " + str(random.randint(1,20))
    return address
    

#
# Wähle zufällig einen Einsatz aus
# Diese sind dabei gewichtet:
# größeres Level -> größere Häufigkeit
# kleineres Level -> kleinere Häufigkeit
#
def choose_task():

    freq = [row["Level"] for row in tasks_pool]
    weights = [float(i) for i in freq]
    choosen_task = random.choices(tasks_pool, weights=weights)[0]

    msg_short = choosen_task['\ufeffstichwort']
    msg_text = choosen_task['stichwort_text']
    description = choosen_task['beschreibung']
    
    return msg_short, msg_text, description
    