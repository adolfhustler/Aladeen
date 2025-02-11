from cryptography.fernet import Fernet


key = b"KzgB8bcSmuhiXudpeJ97pGxrVJNpRUAeeKR7MK80hbQ="
cipher_suite = Fernet(key)

discord_token = "MTMzNTExNTU1ODYzODcxOTA4OA.G-2ZV5.Yi0lHbM3jRt_cy0DP3YXbww-8SlCMKoprbOB6Q"


encrypted_token = cipher_suite.encrypt(discord_token.encode())


print("Encrypted Token:", encrypted_token.decode())