import datetime
import os

home_dir = os.path.expanduser("~")
log_path = home_dir + "/FireboardTaskGenerator/output.log"

def log(message):
    log_entry = f"{datetime.datetime.now()} - {message}\n"
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
