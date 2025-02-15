from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("25657194"))
API_HASH = getenv("cee5bdd9803dc1fbac282863204bdfec")
BOT_TOKEN = getenv("7892423173:AAFLR_hwGjpFjIdV39d9rxEcOyul9JwYpI0")
BOT_USERNAME = getenv("Venomcbot")
OWNER_ID = int(getenv("7900262575"))
LOGGER_ID = int(getenv("-1002107679944
"))
MONGO_URL = getenv("mongodb+srv://surajit69697:surajit69697@cluster0.7rwzn.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

SUDOERS = filters.user([7900262575,1883889098,7638575366])
