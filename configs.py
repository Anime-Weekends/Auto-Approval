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
    STRING_SESSION = os.getenv("STRING_SESSION", "BQCak1gAoahiNjgVkG8BLg585T_qMfITz_H0zk4TS7jr4sgfRpdJLI7hcCONDfFMhNpk36g0E1nioW7C2Ye3OiFjKLrpKEbLS5Q-nAn4pu6ueRW8c1AvDK-mZaELlIVMvPAE_GIpFFuli3OCojoPOe779I2vrldE-s4N3_0AN-mrQLbPvXctSv9pQqkcCe1ttuOfcOROUk225WK1ffXpDlzPvXB8RQjF4gX9e2ADXFK-5snRVoTu52jd2gYokc2S3EcmzQC_EtQPO40wtQKvFMMR91iBVv3dA-yVQLfi9Y-ZMi48K3pIX5h5-Pc8IJAKaXv97TUITHTBZYTAVDy-Oc9aJeMK2AAAAAGmk-HvAA")

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
