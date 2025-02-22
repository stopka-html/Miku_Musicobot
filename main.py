from __future__ import unicode_literals
import ffmpeg
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
import nacl
import music_list
import keys
TOKEN = keys.TOKEN
client = commands.Bot(command_prefix = '.', intents = discord.Intents.all())
list_of_playlists = {}

music_list.load_list()
    

async def play_playlist(ctx):
        while list_of_playlists[ctx.guild.id]["url"]:
            
            i = list_of_playlists[ctx.guild.id]["url"].pop(0)
            if i not in music_list.music_list:
                await ctx.send("Downloading...")
                music_list.acess_await(i)
                while i not in music_list.music_list:
                    await asyncio.sleep(2)
                await ctx.send("Downloaded!")
            source = FFmpegPCMAudio(music_list.music_list[i]["filename"])
            embed = discord.Embed(title="Now playing <:a_anime_blush_cute_kawaii_uwu:1239615541216415837>", description=music_list.music_list[i]["name"], color=0x00FF00)
            await ctx.send(embed=embed)
            
            player = list_of_playlists[ctx.guild.id]["voice"].play(source)
            j = 0
            #for j in range(round(float(ffmpeg.probe(music_list.music_list[i]["filename"])['format']['duration']))+1):
            while j <= round(float(ffmpeg.probe(music_list.music_list[i]["filename"])['format']['duration']))+1:
                await asyncio.sleep(1)
                j += 1
                if "skip" in list_of_playlists[ctx.guild.id] and list_of_playlists[ctx.guild.id]["skip"]:
                    list_of_playlists[ctx.guild.id]["skip"] = False
                    list_of_playlists[ctx.guild.id]["voice"].stop()
                    break
                    
                if "pause" in list_of_playlists[ctx.guild.id] and list_of_playlists[ctx.guild.id]["pause"]:
                    print(j,"before")
                    j -= 1
                    print(j,"after")
                    continue    
                
            print(list_of_playlists[ctx.guild.id]["url"]) 
        await stop(ctx)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')    


@client.command(name="playit")
async def play(ctx,url):
    channel = ctx.message.author.voice.channel
    try:
        voice = await channel.connect()
    except:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if ctx.guild.id not in list_of_playlists:
        print("creating_playlist")
        list_of_playlists[ctx.guild.id] = {"url": [url], "voice": voice, "skip": False, "pause": False}
        asyncio.create_task(play_playlist(ctx))
    else:
        print("adding_to_playlist")
        list_of_playlists[ctx.guild.id]["url"].append(url)
    
# STOP sound and quit
@client.command(name="stop")
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await voice.disconnect()
    list_of_playlists.pop(ctx.guild.id)
    embed = discord.Embed(title="Stopped, BYE!! <:AP_uwu:1239616304454045806>", color=0x00FF00)
    await ctx.send(embed=embed)



# SKIP song
@client.command(name="skipit")
async def skip(ctx):
    if ctx.guild.id in list_of_playlists:
        list_of_playlists[ctx.guild.id]["skip"] = True



# PAUSE
@client.command(name="pause")
async def pause(ctx):
    if ctx.guild.id in list_of_playlists:
        list_of_playlists[ctx.guild.id]["pause"] = True if list_of_playlists[ctx.guild.id]["pause"] == False else False
        if list_of_playlists[ctx.guild.id]["pause"]:
            list_of_playlists[ctx.guild.id]["voice"].pause()
        else:
            list_of_playlists[ctx.guild.id]["voice"].resume()
        embed = discord.Embed(title="Paused" if list_of_playlists[ctx.guild.id]["pause"] else "Resumed", color=0x00FF00)
        await ctx.send(embed=embed)
            


# QUEUE 
@client.command(name="queue")
async def queue(ctx):
    if ctx.guild.id in list_of_playlists:
        embed = discord.Embed(title="Now playing", color=0x00FF00)
        for i in list_of_playlists[ctx.guild.id]["url"]:
            try:
                embed.add_field(name=music_list.music_list[i]["name"], value=i, inline=False)
            except:
                embed.add_field(name="downloading", value=i, inline=False)
        await ctx.send(embed=embed)

client.run(TOKEN)
