import discord, os
from dotenv import load_dotenv
from discord.ext import commands
import music
import extra

load_dotenv()

cogs = [music, extra]

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@client.event
async def on_ready():
    for i in range(len(cogs)):
        await cogs[i].setup(client)
    print('Geisha: Ready to go!')

TOKEN = os.getenv('TOKEN')
client.run(TOKEN)
