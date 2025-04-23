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
    STRING_SESSION = os.getenv("STRING_SESSION", "BQG2mwYAf3DF9RzUKBx_ey01hdgqCYToVg8w-0TGWntQnq7QSwr3_Nz8Agk7oGmAqAJyV6-SaTjr1MLPgi8NBarag-Uc0CRHxRNhVM3Nh-ZWOW10JUEwXtJksQMw9lW_ci7Hj49a9DswedSOJ550dAeo74EFGLlccz4Y_5kpY7X_dWp63CIp4jxhz0EWsiibfNccVwrFctv2y9AAS4Reiy-mEEK2jTmx-Xx1tJXJ9x5bIO-eru7Wl2OloVyenq-11ttTs21M9GB9L5lKKhmDDvUSZVOjm30F0fnH2Pioftfy7J4SkRe_Hqxj5B7Q4Xh6vTujK7pwzZCk-Tz7qBYYVpNLfTP3IwAAAAF1g6UNAA")

    # Admin User IDs
    SUDO = list(map(int, os.getenv("SUDO", "5548954124 6429532957").split()))
    
    # MongoDB URI
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority"
    )

cfg = Config()
