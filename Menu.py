#
# author = Nils Ommen
# date = 07.08.2023
# version = 1.0
# application use = fireboard api access
# 
# Menu.py

from tabulate import tabulate

from Task_Class import Task
from Task_Manager import *
from Fireboard_Task import FireboardTask

tasks = []

cmd_stack = []

import_streets()
import_tasks()

#
# Function from the menu
#
def create_task_from_pool():
    address = choose_street()
    msg_short, msg_text, description = choose_task()

    task = Task(address, msg_short, msg_text)
    tasks.append(task)

    fire_task = FireboardTask(task, description, len(tasks))
    # deactivate the api access here:
    fire_task.send_task_to_api()
    print("Done")

def add_car_func(cmd_splitted):
    if not cmd_splitted[1].isdigit():
        raise TypeError("arg 2 was not a digit")
            
    line = int(cmd_splitted[1]) - 1
    print(tasks[line])
    tasks[line].add_car(cmd_splitted[2])

def add_info_func(cmd_splitted):
    if not cmd_splitted[1].isdigit():
        raise TypeError("arg 2 was not a digit")
    
    line = int(cmd_splitted[1]) - 1
    kommentar = ' '.join(cmd_splitted[2:])
    tasks[line].add_info(kommentar)

def change_status_func(cmd_splitted):
    if not cmd_splitted[1].isdigit():
        raise TypeError("arg 2 was not a digit")
    
    line = int(cmd_splitted[1]) - 1
    taskHasEnded = tasks[line].set_next_status(cmd_splitted[2])
    if taskHasEnded:
        del tasks[line]

def undo_func():
    prev_cmd = cmd_stack.pop().split(' ')
    task_num = -1
    if len(prev_cmd) > 1 and prev_cmd[1].isdigit():
        task_num = int(prev_cmd[1]) - 1

        if(prev_cmd[0] == "fzg"):
            tasks[task_num].delete_last_car()            
        elif(prev_cmd[0] == "info"):
            tasks[task_num].delete_last_info()
        else:
            raise RuntimeError("can't undo the last command")
    else:
        raise RuntimeError("can't reconstruct the cmd")
    
def print_help():
    print("--- BEFEHLE: ---")
    print("einsatz")
    print("fzg <zeile> <rufname>")
    print("info <zeile> <kommentar>")
    print("status <zeile> <fahrzeug rufnummer>")
    print("undo")
    print("exit")
    print("\n")

    input("Weiter mit Enter...")

def main_menu():
    cmd = input("Befehlseingabe: ")

    cmd_splitted = cmd.split(' ')

    try:
        match cmd_splitted[0]:
            case 'einsatz':
                create_task_from_pool()

            case 'fzg':
                add_car_func(cmd_splitted)

            case 'info':
                add_info_func(cmd_splitted)

            case 'status':
                change_status_func(cmd_splitted)

            case 'undo':
                undo_func()
                
            case 'help':
                print_help()
            
            case 'exit':
                exit()

            case _:
                raise Exception("Unkown Command")

    except Exception as err:
        print(f"Error handling your command: {err=}, {type(err)=}")
        input("Weiter mit Enter...")

    finally:
        if(cmd_splitted[0] == "fzg" or cmd_splitted == "info"):
            cmd_stack.append(cmd)

def print_info():
    print("--- Menu ---")
    print("'help' um alle Befehle zu zeigen \n")

def print_table():
    task_table = [['#', 'Adresse', 'Stichwort', 'Stichwort Text', 'Infos', 'Fahrzeuge', 'Status']]

    for idx, task in enumerate(tasks):
        infos = "\n".join(task.get_infos())
        cars_name = "\n".join(task.get_cars_name())
        cars_status = "\n".join(task.get_cars_status())
        
        task_table.append([
            str(idx + 1),
            task.get_address(), 
            task.get_message_short(), 
            task.get_message_text(), 
            infos, 
            cars_name,
            cars_status
        ])
        
    print(tabulate(task_table, headers='firstrow', tablefmt='grid'))
