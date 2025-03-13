# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01


from os import path, getenv

class Config:
    API_ID = int(getenv("API_ID", "28744454"))
    API_HASH = getenv("API_HASH", "debd37cef0ad1a1ce45d0be8e8c3c5e7")
    BOT_TOKEN = getenv("BOT_TOKEN", "7953776996:AAHKLreBz3nDUCEScfK3lNB8EMoSfvq4QxA")
    # Your Force Subscribe Channel Id Below 
    CHID = int(getenv("CHID", "-1002410513772")) # Make Bot Admin In This Channel
    # Admin Or Owner Id Below
    SUDO = list(map(int, getenv("SUDO", "5548954124 6429532957 6266529037").split()))
    MONGO_URI = getenv("MONGO_URI", "mongodb+srv://jeffysamaweekends:jeffysamaweekends@cluster0.ulyfw.mongodb.net/?retryWrites=true&w=majority")
    
cfg = Config()

# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01
