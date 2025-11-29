import discord, os
from dotenv import load_dotenv
from discord.ext import commands
from google import genai
from ai import aicog
import music
import extra

load_dotenv()
GEM_KEY = os.getenv('GEM_API')

cogs = [music, extra]

gemmy = genai.Client(api_key=GEM_KEY)
MODEL = 'gemini-2.5-flash'

client = commands.Bot(command_prefix = "!", intents = discord.Intents.all())

@client.event
async def on_ready():
    await client.add_cog(aicog(client, gemmy, MODEL))
    for i in range(len(cogs)):
        await cogs[i].setup(client)
    print('Geisha: Ready to go!')

TOKEN = os.getenv('BOT_TOKEN')
client.run(TOKEN)
