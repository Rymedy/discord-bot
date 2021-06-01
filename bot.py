import discord
from discord.ext import commands
import youtube_dl
import os

client = commands.Bot(command_prefix = '.', description='Hi')

@client.event
async def on_ready():
    print('The bot has logged in!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dhar mann | .commands"))

@client.event
async def on_member_join(member):
	print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
	print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
	await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

@client.command()
async def dhar(ctx):
	await ctx.send("https://www.youtube.com/channel/UC_hK9fOxyy_TM8FJGXIyG8Q")

@client.command()
async def commands(ctx):
    await ctx.send("```Standard Commands:\n.ping -- shows connection latency\n.clear -- purges 5 recent messages\n.dhar -- gives link to dhar mann's channel\n\nMusic Commands:\n.play {{URL}} -- plays a song off youtube\n.leave -- disconnects the bot from the voice channel\n.pause -- pauses the song current being played\n.resume -- resumes the song that is paused\n.stop -- stops the song being played```")

# Music and Youtube related commands etc.
@client.command()
async def play(ctx, url : str):
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
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Currently no audio is playing.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("The audio is not paused.")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

client.run('ODQ5MTY5NTE4MzAyODU1MTc4.YLXQvQ.F2YFujbMYyO51iDCIcOPf9hWP8A')
