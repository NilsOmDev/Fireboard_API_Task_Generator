#
# author = Nils Ommen
# date = 07.08.2023
# version = 1.0
# application use = fireboard api access
# 
# Main.py

import os
from Menu import *

auth_key = ''       # insert your API authentication key here

if __name__ == '__main__':
    print("Starting...")

    while(True):
        os.system('cls')
        print_table()
        print_info()
        main_menu()