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
    BOT_USERNAME = os.getenv("BOT_USERNAME", "AutoAnimeNews_Bot")
    
    # Add your string session here
    STRING_SESSION = os.getenv("STRING_SESSION", "BQGcIrIAOh8-Sqw77vfX0IcZSH_BFbZUDCkRFeQfQfLKSMm2IB52qDSJepEwCp25OVYPgOVcH0-dZS2ImqlWJA8QLPL6v5XdGX7-1bun5CtY11nmBGTi4VANhtBJ4be8PeZsMzUDnLUFtoqCuoZm_xTszs6iySjUaHIHrvgV9MssqbcCJ_bScnTc1lyEHsX3SFSugL3Tw6V6LXgUqYN3EeASpt-Fanb-MQ6ObVoG8KazZZUyunsRSgR5JAqqz-wyvBAnFx7lelilMzLsmZRcmK1r1l9ub6zjpVhvQ0X8D1bcQu37Gz7_laxsKHrtJfhUwkIntdufk2zIy3mkJuYa3J459cg9dAAAAAF_OuMdAA")

    # Force Subscribe Channel ID (Ensure bot is admin)
    FORCE_SUB_CHANNELS = list(map(int, os.getenv("FORCE_SUB_CHANNELS", "-1002410513772 -1002296091847").split()))
    
    # Admin User IDs
    SUDO = list(map(int, os.getenv("SUDO", "5548954124 6429532957").split()))
    
    # MongoDB URI
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority"
    )

    # Log Channel ID
    LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "-1002182302693"))  # Your Log Channel ID here

cfg = Config()
