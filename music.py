import discord
from discord.ext import commands
import yt_dlp
import random
import re
import json

queue = []
track = []
nowPlaying = ""
class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    def check_queue(self, ctx):
        global nowPlaying, queue
        if queue:
            vc = ctx.voice_client
            source = queue.pop(0)
            nowPlaying = track.pop(0)
            vc.play(source, after=lambda x=None: self.check_queue(ctx))

    async def loadsong(self, ctx, source, name, isList):
        global nowPlaying
        vc = ctx.voice_client
        if vc.is_playing():
                track.append(name)
                queue.append(source)

                #added "if" statement so it doesn't spam chat atm
                if not isList:
                    await ctx.send("Added to queue!")
        else:
            nowPlaying = name
            vc.play(source, after=lambda x=None: self.check_queue(ctx))
            await ctx.send("Oki Doki!")
    
    def convertToString(self, num, name):
        str = num + ")  " + name
        return str

    @commands.command()
    async def dc(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I've already been abandoned.")
        else:
            await ctx.voice_client.disconnect()
            await ctx.send("Bye Bye!")

    @commands.command()
    async def summon(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Join a voice channel!")
        else:
            await ctx.author.voice.channel.connect()
            await ctx.send("Greetings.")

    @commands.command()
    async def pause(self, ctx):
        try:
            if ctx.voice_client.is_paused():
                await ctx.send("You Been Paused Foo.")
                return

            ctx.voice_client.pause()
            await ctx.send("Pausing Bangers...")
        except:
            await ctx.send("No Hay Musica Sonando!")

    @commands.command()
    async def resume(self, ctx):
        try:
            if ctx.voice_client.is_playing():
                await ctx.send("Estas Sordo?")
                return

            ctx.voice_client.resume()
            await ctx.send("Resuming Bangers!")
        except:
            await ctx.send("No Hay Musica Sonando!")

    @commands.command()
    async def skip(self, ctx):
        try:
            ctx.voice_client.stop()
            await ctx.send("Song skipped!")
        except:
            await ctx.send("No trash to skip!")

    @commands.command()
    async def play(self, ctx, *, url):
        global nowPlaying
        url2 = None
        #vidgex = re.compile("=251&")
        listgex = re.compile("playlist")

        if ctx.author.voice is None:
            await ctx.send("Join a voice channel!")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
                                            #put -re before -reconnect 1
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format' : 'bestaudio/best', 'age_limit' : 21} #'dump_single_json' : 'True', 'extract_flat' : 'True'
        
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            #if NOT a playlist then do this                                                                                         
            if not(re.search(listgex, url)):             
                try:
                    info = ydl.extract_info(url, download=False)
                except:
                    info = ydl.extract_info(f"scsearch:{url}", download=False)['entries'][0] #ytsearch:{url} (for youtube)
                #This is old format to get direct link (doesn't work)
                #for item in info['formats']:
                    #if(re.search(vidgex, item['url'])):
                        #url2 = item['url']
                        #break

                info = ydl.sanitize_info(info)
                if url2 == None:
                    url2 = info['url']
                    #url2 = info['formats'][0]['url']

                source = await discord.FFmpegOpusAudio.from_probe(url2, ** FFMPEG_OPTIONS)
                name = info.get("title")

                print(source) #debug line

                #Bool is asking if it is a playlist
                isList = False
                await self.loadsong(ctx, source, name, isList)

            else:
                print("Hooray!")
                info = ydl.extract_info(url, download=False)
                count = info.get("playlist_count")
                for x in range(count):
                    for item in info['entries'][x]['formats']:
                        if(re.search(vidgex, item['url'])):
                            url2 = item['url']
                            source = await discord.FFmpegOpusAudio.from_probe(url2, ** FFMPEG_OPTIONS)
                            name = info['entries'][x]['title']

                            print(source) #debug line

                            isList = True
                            await self.loadsong(ctx, source, name, isList)

    @commands.command()
    async def queue(self, ctx, show: int = 20):
        #make it so you can change pages of the queue
        #also when there are no songs playing make queue status to show as such
        embed = discord.Embed(
            colour=ctx.author.colour,
        )
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.display_name}")
        embed.add_field(
            name="Now Playing",
            value="\n" + nowPlaying,
            inline=False
            )
        if queue:
            embed.add_field(
            name="Next up",
            value="\n".join(self.convertToString(str(x+1), track[x]) for x in range(len(track[:show]))),
            inline=True
            )
        else:
            embed.add_field(
            name="Next up",
            value="\n" + "Empty!",
            inline=True
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        queue.clear()
        track.clear()
        await ctx.send("Queue cleared!")

    @commands.command()
    async def swap(self, ctx, x, y):
        one = int(x)-1
        two = int(y)-1
        temp = queue[two]
        queue[two] = queue[one]
        queue[one] = temp

        temp = track[two]
        track[two] = track[one]
        track[one] = temp
        await ctx.send("Done!")

    @commands.command()
    async def move(self, ctx, x, y):
        start = int(x)-1
        final = int(y)-1
        qTemp = queue[start]
        tTemp = track[start]

        #fix this, it doesnt work right if you try moving song early in queue with another
        #later in queue ex: !move 2 4
        if(start > final):
            for i in reversed(range(start-final)):
                queue[i+1] = queue[i]
                track[i+1] = track[i]
        else:
            for i in range(final-start):
                queue[i] = queue[i+1]
                track[i] = track[i+1]
        queue[final] = qTemp
        track[final] = tTemp
        await ctx.send("You're Welcome.")

    @commands.command()
    async def shuffle(self, ctx):
        global queue, track
        both = list(zip(queue, track))
        random.shuffle(both)
        tQueue, tTrack = zip(*both)

        queue = list(tQueue)
        track = list(tTrack)
        await ctx.send("Scrambled Like An Egg!")

    @commands.command()
    async def remove(self, ctx, remove):
        re = int(remove)
        try:
            queue.pop(re-1)
            track.pop(re-1)
            await ctx.send("Song Vanquished!")
        except IndexError:
            await ctx.send("Nani?")

  
async def setup(client):
    await client.add_cog(music(client))
