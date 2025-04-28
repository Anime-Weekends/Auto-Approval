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
    STRING_SESSION = os.getenv("STRING_SESSION", "BQCak1gAR3lRXlZuUbkbGz92-qsDWHjOhPrZUGvg5KAn4LQfJHeARt7ugPXcLLP2pI3VZCx6dUE2M2mCtfUTiGwor_qg5ox2ejQ2BnV7PJFbfizAOR8AaCkUTv-C1A0tJtGDSjPis3wDNj5bVX1J0j5VAjBLCVxzreDlUq31Ekg3_DCGPkWNeWd-emiVg1po0PS2kG1oFVcDiva8IGy7t8HaWanI4rGx3XZ4m8yr1txbBv_-WEYUkGvb3u8gDK4kwtYOIDmo7_n-DG4uaO6ff5nyiY5zZzS8qFJwetT5Q5X1jtZYscEFAaxFeiVq_d1fL4jZZ3fIRAEBy_cZ284_Wx4KW5OPDQAAAAGmk-HvAA")

     # Force Subscribe Channel ID (Ensure bot is admin)
    FORCE_SUB_CHANNELS = list(map(int, os.getenv("FORCE_SUB_CHANNELS", "-1002410513772 -1002296091847").split()))
    
    # Admin User IDs
    SUDO = list(map(int, os.getenv("SUDO", "5548954124 6429532957").split()))
    
    # MongoDB URI
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority"
    )

cfg = Config()
