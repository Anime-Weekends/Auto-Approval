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
    STRING_SESSION = os.getenv("STRING_SESSION", "BQCak1gAjmw-jxxKeNYIPEY9oaSTeWbUIHvyv7pFoirTqVVThW3ve1LKTFXEbi7xmKOMVGJsGL_JIKl-40IPYBcnYEM1M1mnDJ0eZO0FkuHGmmjoHrix9XeHPHKfYJ1riY_AnRXJwPAcqc66xu8D0HxFEPMa2WqEbc950jlCRFZCcJ-HdlFYJLQ2k0Be5HxBHbfIaqlH1H3mDV7kEQg681GuD7L7TS3X99keV9LDr_ZGnaRNeQIeWthYvDSrc7QxYjQesAG7E4UsTl7JAJ-8b5mTs07qqRrG4Ylg4ALUSWu5hp8lt-Qmfyi8PYIFULIb5maqThr0CLP-lEig5SK3Xg66_51JvwAAAAGmk-HvAA")

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
