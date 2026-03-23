import discord
from discord.ext import commands
import datetime
import os

# -----------------------------
# CONFIGURATION
# -----------------------------

OWNER_ID = 1350160061967630399 

TRACKED = [
    1035868089173192815,
    1462670187231969301,
    1472532965199184011
]

# -----------------------------
# BOT SETUP
# -----------------------------

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_update = {}

def log(msg):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] {msg}")

# -----------------------------
# EVENTS
# -----------------------------

@bot.event
async def on_ready():
    log(f"Bot connecté en tant que {bot.user}")
    log("Suivi des utilisateurs :")
    for uid in TRACKED:
        log(f" - {uid}")

@bot.event
async def on_presence_update(before, after):
    if after.id not in TRACKED:
        return

    uid = after.id
    now = datetime.datetime.now()

    # Récupérer l'utilisateur qui reçoit les alertes
    owner = await bot.fetch_user(OWNER_ID)

    # Première fois qu'on voit cet utilisateur
    if uid not in last_update:
        last_update[uid] = now
        return

    # -----------------------------
    # 1) CHANGEMENT DE STATUT
    # -----------------------------
    if before.status != after.status:
        msg = f"[STATUS] {after.name} : {before.status} → {after.status}"
        log(msg)
        await owner.send(msg)
        last_update[uid] = now
        return

    # -----------------------------
    # 2) CHANGEMENT D'ACTIVITÉ
    # -----------------------------
    before_act = before.activity.name if before.activity else "None"
    after_act = after.activity.name if after.activity else "None"

    if before_act != after_act:
        msg = f"[ACTIVITY] {after.name} : {before_act} → {after_act}"
        log(msg)
        await owner.send(msg)
        last_update[uid] = now
        return

    # -----------------------------
    # 3) SILENT UPDATE
    # -----------------------------
    delta = (now - last_update[uid]).total_seconds()

    if delta > 5:
        msg = f"[SILENT] {after.name} vient de se CONNECTER (invisible possible)"
    else:
        msg = f"[SILENT] {after.name} vient de se DECONNECTER (invisible possible)"

    log(msg)
    await owner.send(msg)

    last_update[uid] = now

# -----------------------------
# RUN
# -----------------------------

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
