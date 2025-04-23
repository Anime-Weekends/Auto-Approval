# ============================================
#             BOT CONFIGURATION FILE
# --------------------------------------------
# This file holds environment-based settings
# required to run the Telegram bot securely.
# ============================================

import os

class Config:
    API_ID = int(os.getenv("API_ID", "28744454"))
    API_HASH = os.getenv("API_HASH", "debd37cef0ad1a1ce45d0be8e8c3c5e7")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7773900178:AAEQEQAXahfYAVsol1EUcwYPKa0Or2cPCdg")
    
    # Force Subscribe Channel ID (Ensure bot is admin)
    CHID = int(os.getenv("CHID", "-1002410513772"))
    
    # Add your string session here
    STRING_SESSION = os.getenv("STRING_SESSION", "BQG2mwYAgxsHqkyxZSAOLyQAb1EkvktN-w5rw-e_CInEL99lVDK2TzAAhn4DDd5hjlC4FqqGC0OSkkkBLXj6K3pnXF-IKNLbhAHx4U8QTttNb-MWZmnjBKgukjjk76u6uQc5McpplXy_yhHj6_QTh7SKL_nlY-daIl-nRIgl3v6OEP1WgSdmDS0dUAfrNbJ1WkuHfBpsKROcVatevupX6trdJONPaZwgdPrKOlfFEl4aAJItyPcj5_lnAkfBC9kn7xWl-dEo-xi51QjCDCJ0hFsXxC-vRHqr-YMxR6uAsdc0tWlAdVDG-2SKx4Mqz7XhTZGeKkVYcj4Gp6kxpvVmTYeK-jdibQAAAAF1g6UNAA")

    # Admin User IDs
    SUDO = list(map(int, os.getenv("SUDO", "5548954124 6429532957").split()))
    
    # MongoDB URI
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority"
    )

cfg = Config()
