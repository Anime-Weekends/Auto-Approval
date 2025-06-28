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
    STRING_SESSION = os.getenv("STRING_SESSION", "BQCak1gAa4ArrhofSrskJiuShYW5QbYd1h-NIS_9w5IoMM7kL5rtVf8KOnT2IVFfdvSsz1sHnXh8ZRPYo3m2SMCQiu3uMThakFf9hCEygPIqTp9s-n5hfFrhryZ1ExC7SH2lPdA3NK5tA0pyh4gLTWiXd4M-PQACCaotkTW3ibe0VSHCZ0699bhiXdAFY3Oa0A40-mA83QpZqNqCZLJuN8SQbwioWh36x9-AEXBZ_rElBquXBSlJHeZv-DcYZChmfRI-FufzWtx-jCZcMKg_HwMMdNuwNH4eMC0Hz5oaBPP9ucwAFe4B1U9hjfXRYsF1etNemQrFzcVCdusfeyfpxuI6XizzoQAAAAGmk-HvAA")

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
