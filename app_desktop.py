import subprocess
import time
import socket
import psutil
import webview

def kill_existing_streamlit():
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['cmdline'] and "streamlit" in proc.info['cmdline'][0]:
                proc.kill()
        except:
            pass


def wait_for_port(port, host="localhost", timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return True
        time.sleep(0.3)
    return False


def start_streamlit():
    return subprocess.Popen(
        ["streamlit", "run", "streamlit_app/streamlit_app.py", "--server.headless=true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )


def stop_process(proc):
    try:
        if proc and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
    except Exception:
        proc.kill()


# ---------------------------------------------
# Ablauf
# ---------------------------------------------
kill_existing_streamlit()
proc = start_streamlit()
if not wait_for_port(8501, timeout=20):
    stop_process(proc)
    raise RuntimeError("Streamlit startete nicht rechtzeitig!")

window = webview.create_window("Fireboard Task Generator", "http://localhost:8501")

def on_close():
    stop_process(proc)

window.events.closed += on_close

webview.start()
