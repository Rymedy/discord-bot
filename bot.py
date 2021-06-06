import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import youtube_dl
from riotwatcher import LolWatcher
import os
import random
import time
import json

client = commands.Bot(command_prefix = '.', description='Commands:')
start_time = time.time()
key = "TOKEN-KEY"
watcher = LolWatcher(key)

client.blacklisted_users = []

@client.command()
async def lol(ctx, summonerName : str):
    print(f".lol was used by user with id: {user_id}")
    summoner = watcher.summoner.by_name('oc1', summonerName)
    stats = watcher.league.by_summoner('oc1', summoner['id'])
    if len(stats) > 1:
        stats = stats[1]
    else:
        stats = stats[0]

    tier = stats['tier']
    rank = stats['rank']
    lp = stats['leaguePoints']

    wins = int(stats['wins'])
    losses = int(stats['losses'])

    winrate = int((wins / (wins + losses)) * 100)

    await ctx.send(f'**{summonerName}** is currently ranked in **{str(tier)} {str(rank)}** with **{str(lp)}LP** and a **{str(winrate)}%** winrate.')

@client.command()
@commands.is_owner()
async def shutdown(ctx):
    print(f".shutdown was used by user with id: {user_id}")
    await ctx.send("The bot has shutdown.")
    await ctx.client.logout()

@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    data = read_json("blacklist")
    client.blacklisted_users = data["blacklistedUsers"]
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dhar mann | .commands"))



@client.command(description='Display an op.gg lookup of inputted players')
async def opgg(ctx, *args):
    print(f".opgg was used by user with id: {user_id}")
    """Pull up op.gg for players"""
    url = 'http://oce.op.gg/'

    if len(args) == 1:
        url += 'summoner/userName=' + args[0]
    elif len(args) > 1:
        url += 'multi/query=' + args[0]
        for i in range(1, len(args)):
            url += '%2C' + args[i]

    await ctx.send(url)

@client.event
async def on_member_join(member):
	print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
	print(f'{member} has left a server.')

@client.event
async def on_message(message):
    global user_id
    user_id = message.author.id
    #ignore ourselves
    if message.author.id == client.user.id:
        return

    #blacklist system
    if message.author.id in client.blacklisted_users:
        return

    if message.content.lower().startswith("help"):
        await message.channel.send("Hey! Why don't you run the help command with '.help")

    await client.process_commands(message)

@client.command()
@commands.is_owner()
async def blacklist(ctx, user: discord.Member):
    print(f".blacklist was used by user with id: {user_id}")
    if ctx.message.author.id == user.id:
        await ctx.send("Hey, you cannot blacklist yourself!")
        return

    client.blacklisted_users.append(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].append(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"Hey, I have **blacklisted** {user.name} for you.")

@client.command()
@commands.is_owner()
async def unblacklist(ctx, user: discord.Member):
    print(f".unblacklist was used by user with id: {user_id}")
    client.blacklisted_users.remove(user.id)
    data = read_json("blacklist")
    data["blacklistedUsers"].remove(user.id)
    write_json(data, "blacklist")
    await ctx.send(f"Hey, I have **unblacklisted** {user.name} for you.")


@client.command()
async def ping(ctx):
    print(f".ping was used by user with id: {user_id}")
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
@commands.has_role('botPerms')
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

@client.command()
async def dhar(ctx):
	await ctx.send("https://www.youtube.com/channel/UC_hK9fOxyy_TM8FJGXIyG8Q")

@client.command(pass_context = True)
@commands.has_role('botPerms')
async def fart(ctx):
    print(f".fart was used by user with id: {user_id}")
    channel = discord.utils.get(ctx.guild.voice_channels, name='CHANNEL')
    voice = await channel.connect()
    source = FFmpegPCMAudio('Sounds/soundreverb.mp3')
    player = voice.play(source)
    time.sleep(1.34)
    if voice.is_connected():
        await voice.disconnect()

@client.command(pass_context = True)
@commands.has_role('botPerms')
async def sheesh(ctx):
    print(f".sheesh was used by user with id: {user_id}")
    channel = discord.utils.get(ctx.guild.voice_channels, name='CHANNEL')
    voice = await channel.connect()
    source = FFmpegPCMAudio('Sounds/sheesh.mp3')
    player = voice.play(source)
    time.sleep(6.5)
    if voice.is_connected():
        await voice.disconnect()


@client.command()
async def ppsize(ctx):
    print(f".ppsize was used by user with id: {user_id}")
    responses = ['8=D',
                '8==D',
                '8===D',
                '8====D',
                '8=====D',
                '8======D',
                '8=======D',
                '8========D',
                '8=========D',
                '8==========D',
                '8===========D',
                '8============D',
                '8=============D',
                '8===========================================D']
    await ctx.send(f'PP Size:\n{random.choice(responses)}')

@client.command()
async def dm(ctx):
    print(f".dm was used by user with id: {user_id}")
    await ctx.send("Check your DM's.")
    await ctx.author.send("free hentai :)")
    await ctx.author.send("https://twitter.com/SokaroAU/likes")

@client.command(description='Display the uptime of the bot')
async def up_time(ctx):
    print(f".uptime was used by user with id: {user_id}")
    await ctx.send(str(int(time.time() - start_time)) + ' seconds')

@client.command()
async def commands(ctx):
    print(f".commands was used by user with id: {user_id}")
    await ctx.send("```**Standard Commands:**\n.uptime -- shows how long the bot has been online\n.ping -- shows connection latency\n.clear -- purges 5 recent messages\n.dhar -- gives link to dhar mann's channel\n.fart -- plays fart reverb sound effect in the 'doms restroom' channel.\n.sheesh -- plays uto sheeeshee sound effect\n.ppsize -- shows pp size\n.dm -- sends a mysterious link\n\n**Music Commands:**\n.play {{URL}} -- plays a song off youtube\n.leave -- disconnects the bot from the voice channel\n.pause -- pauses the song current being played\n.resume -- resumes the song that is paused\n.stop -- stops the song being played\n\n**League of Legends Commands:**\n.lol -- shows league rank\n.opgg -- sends op.gg stats link and can take more than 1 argument\n```")

# Music and Youtube related commands etc.
@client.command()
async def play(ctx, url : str):
    print(f".play was used by user with id: {user_id}")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            await voice.disconnect()
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return

    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='doms restroom')
    await voiceChannel.connect()
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    await ctx.send(f'Now playing: {url}')


@client.command()
async def leave(ctx):
    print(f".leave was used by user with id: {user_id}")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    print(f".pause was used by user with id: {user_id}")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send("The current song has been paused.")
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    print(f".resume was used by user with id: {user_id}")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        await ctx.send("The current song has been resumed.")
    else:
        await ctx.send("The audio is not paused.")

@client.command()
async def stop(ctx):
    print(f".stop was used by user with id: {user_id}")
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
    await ctx.send("The current song has been stopped.")

def read_json(file):
    with open(f"blacklist.json", "r") as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    with open(f"blacklist.json", "w") as file:
        json.dump(data, file, indent=4)

client.run('TOKEN-KEY')
