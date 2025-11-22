from Task_Class import Task
from Task_Manager import *
from Fireboard_Task import FireboardTask
import asyncio

import global_vars

tasks = []
cmd_stack = []

import_streets()
import_tasks()
import_cars()

#
# Function from the menu
#
def create_task_from_pool():
    address = choose_street()
    msg_short, msg_text, description = choose_task()
    create_task(address, msg_short, msg_text, description)


def create_task(address, msg_short, msg_text, description):
    task = Task(address, msg_short, msg_text)
    tasks.append(task)

    fire_task = FireboardTask(task, description, len(tasks))

    if global_vars.send_task:
        log("[INFO]: Task generated and send: " + task.get_message_short() + " " + task.get_address())
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fire_task.send_task_to_api())
    else:
        log("[INFO]: Task generated but not send " + task.get_message_short() + " " + task.get_address())

def close_task(line):
    line -= 1
    if line < len(tasks):
        del tasks[line]
    else:
        log("[ERROR]: line not found")
    
def add_car_func(line, car):
    line -= 1
    if line < len(tasks):
        tasks[line].add_car(car)
    else:
        log("[ERROR]: line not found")

def add_info_func(line, info):
    line -= 1
    if line < len(tasks):
        tasks[line].add_info(info)
    else:
        log("[ERROR]: line not found")
    
def change_status_func(line, car):
    line -= 1
    if line < len(tasks):
        taskHasEnded = tasks[line].set_next_status(car)
        if taskHasEnded:
            del tasks[line]
    else:
        log("[ERROR]: line not found")

def undo_func():
    if len(cmd_stack) != 0:
        prev_cmd = cmd_stack.pop().split(' ')
        task_num = -1
        if len(prev_cmd) > 1 and prev_cmd[1].isdigit():
            task_num = int(prev_cmd[1]) - 1

            if(prev_cmd[0] == "fzg"):
                tasks[task_num].delete_last_car()            
            elif(prev_cmd[0] == "info"):
                tasks[task_num].delete_last_info()
            else:
                log("[ERROR]: can't undo the last command")
        else:
            log("[ERROR]: can't reconstruct the cmd")
    else:
        log("[ERROR]: there is no command to undo")
    

def get_table():
    task_table = [['Nr.', 'Adresse', 'Stichwort', 'Stichwort Text', 'Infos', 'Fahrzeuge']]

    for idx, task in enumerate(tasks):
        
        task_table.append([
            str(idx + 1),
            task.get_address(), 
            task.get_message_short(), 
            task.get_message_text(), 
            task.get_infos(), 
            task.get_cars_with_status()
        ])
        
    return task_table

