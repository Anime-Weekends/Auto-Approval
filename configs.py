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
    BOT_USERNAME = os.getenv("BOT_USERNAME", "Private_Auto_Approval_Bot")

    
    # Add your string session here
    STRING_SESSION = os.getenv("STRING_SESSION"," BQCak1gAFNLx21bs_8BSEybPfFn9hsI-owzMuJvIJ8hfF36KwcwaOKzJu57XbUevcX6Mj5BjgLQibOUlQFpGUjhr206RY1ZXDClmQONZrIrntQxaxfxKnO2Guk463gMy4bcDXOULKGJiHB8snLjH_dJ9LvBeXWTcE5BrnYmkOKDCyfxYv0o_NIb0dg3TzPBmnflWV0jRR3M4nmJBue4TMnQChpr9LKq_i0SRZESBWCKLKL8adOJPQfXkFrJPzAV0LXMq9XX-TtPDb3lEcFMj1FFd-6vFUinNds194jfTPmaYp3BnGX5eSWtIcdcs2MFMbNMKTOPo7TUM4wC_OnPUuyblsSpetwAAAAGmk-HvAA")

     # Force Subscribe Channel ID (Ensure bot is admin)
    FORCE_SUB_CHANNELS = list(map(int, os.getenv("FORCE_SUB_CHANNELS", "-1002410513772 -1002296091847").split()))
    
    # Admin User IDs
    SUDO = list(map(int, os.getenv("SUDO", "5548954124 6429532957 6266529037").split()))
    
    # MongoDB URI
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority"
    )

cfg = Config()
