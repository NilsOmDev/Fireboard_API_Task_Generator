import subprocess
import time
import socket
import psutil
import webview
import sys
import os

# -----------------------
# Basis-Pfad ermitteln
# -----------------------
if getattr(sys, 'frozen', False):
    # Bei PyInstaller One-File oder One-Dir
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

streamlit_file = os.path.join(base_path, "streamlit_app", "streamlit_app.py")

# -----------------------
# Hilfsfunktionen
# -----------------------
def kill_existing_streamlit():
    """Beende alle laufenden Streamlit-Prozesse"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and "streamlit" in proc.info['cmdline'][0]:
                proc.kill()
        except:
            pass

def wait_for_port(port, host="localhost", timeout=60):
    """Warte, bis ein Port offen ist (Streamlit gestartet)"""
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.3)
    return False

def start_streamlit():
    """Starte Streamlit-App im Subprozess"""
    return subprocess.Popen(
        ["streamlit", "run", streamlit_file, "--server.headless=true"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def stop_process(proc):
    """Beende Subprozess sauber"""
    try:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
    except Exception:
        proc.kill()

# -----------------------
# Ablauf
# -----------------------
kill_existing_streamlit()
proc = start_streamlit()

if not wait_for_port(8501):
    stop_process(proc)
    raise RuntimeError("Streamlit startete nicht rechtzeitig!")

window = webview.create_window("Fireboard Task Generator", "http://localhost:8501")
window.events.closed += lambda: stop_process(proc)  
webview.start()

