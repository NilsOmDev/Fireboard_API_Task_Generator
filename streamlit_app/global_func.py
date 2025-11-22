import datetime

def log(message):
    log_entry = f"{datetime.datetime.now()} - {message}\n"
    with open("/mnt/output.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
