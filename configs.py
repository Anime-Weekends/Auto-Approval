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
    BOT_TOKEN = os.getenv("BOT_TOKEN", "7953776996:AAEs6kE3z0ryANnheR00EfDb6p-5hdlzriw")
    BOT_USERNAME = os.getenv("BOT_USERNAME", "Private_Auto_Approval_Bot")

    
    # Add your string session here
    STRING_SESSION = os.getenv("STRING_SESSION", "BQCak1gAobzrvty3VVHsZa_pjjIxYwdFhLL6XYjFUDQRcNtTyZOqAD2PZj5Qx_1RJ-PH_hlWEAWx3B1L-IQ7wv1T4N5SRawkys7alm34NJ9qCTNe1iIA44z3d64jnf0bIjel68OlwmmYlM56c-S7Inc0p4s5oV1eFZ1gXyzXVDfKT6NWWkOh6ibbpEy-vPJEiI5TNLLjOJQR09S51373rKA_Px2qL9CxY-Af9cwiUIPABorjOapBfwgnJFRZwBkfsnmUX2JeQdC2k96BAyvYJQRQWaJXOascqXWtLZnEB1gmEXX7GT1hVZU0Q9PiSh0_mpWhGWAesIyAqVzHTLX4ZUApZ9GczgAAAAGmk-HvAA")

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
