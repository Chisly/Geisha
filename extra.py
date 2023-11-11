import discord
from discord.ext import commands
from random import randint
import yt_dlp
import os


class extra(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def secret(self, ctx):
        await ctx.send("President huele a po po.")

    @commands.command()
    async def choose(self, ctx):
        num = randint(1,2)
        if num % 2 == 0:
            await ctx.send("Yay")
        else:
            await ctx.send("Nay")

    @commands.command()
    async def comfort(self, ctx):
        await ctx.send("It'll all work out in the end and know that I will always love you.")

    @commands.command()
    async def download(self, ctx, url):
        YDL_OPTIONS = {'age_limit' : 21,
                       'format': 'bestaudio/best',
                       #Linux Version
                       'outtmpl' : '/home/badpi/Geisha/GeishaExtracts/%(title)s.%(ext)s',

                       #Windows Version
                       #'outtmpl' : 'E:\Coding Projects\Geisha\GeishaExtracts\%(title)s.%(ext)s',

                       'postprocessors': [{
                           'key': 'FFmpegExtractAudio',
                           'preferredcodec': 'mp3',
                           }]
                        }
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download(url)
            #Linux
            dirList = os.listdir('/home/badpi/Geisha/GeishaExtracts/')

            #Windows
            #dirList = os.listdir('E:\Coding Projects\Geisha\GeishaExtracts')
            fileName = dirList[0]

        await ctx.send("Please Wait...")
        #Linux
        await ctx.send(file=discord.File(f'/home/badpi/Geisha/GeishaExtracts/{fileName}'))

        if os.path.exists(f'/home/badpi/Geisha/GeishaExtracts/{fileName}'):
            os.remove(f'/home/badpi/Geisha/GeishaExtracts/{fileName}')

        #Windows
        #await ctx.send(file=discord.File(f'E:\Coding Projects\Geisha\GeishaExtracts\{fileName}'))

        #if os.path.exists(f'E:\Coding Projects\Geisha\GeishaExtracts\{fileName}'):
            #os.remove(f'E:\Coding Projects\Geisha\GeishaExtracts\{fileName}')

        













async def setup(client):
    await client.add_cog(extra(client))
