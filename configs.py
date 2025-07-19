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
    STRING_SESSION = os.getenv("STRING_SESSION", "AQFUFTEArQJhO3y3jpH5-sgcOOQdaAXnh-8KfTyxhcED9k-qGMKyEfZs0hhMWxo8EV7pPDArvibarX51Z1tP6hDiWBIWvp_uvUL2IueKc2c7LpetB8VxN-Ur8RlytLEGF823VbDzxW5X3SLiWoji53AWsWE2VoF_2AeWvuiRfZ_ynfFBDy8EJWw0HW7DLnfsXiKwPFf58p5ah_baGvL25qhnr0xZEuJuZtBd80q_N8wC_mvL4NFbWNT9LLF-Ym3EUBqOIcFEiTK0aMvKwNgaF5sK7NNgX3NvlNqxv9ti_xNrEdeY1dztKKquP8xuC3_QDJc80V485Qa3uRHQe49C52hLoPk3zwAAAAHb5ZnEAA")

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
