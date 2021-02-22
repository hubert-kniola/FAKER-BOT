import discord
import discord.utils
from discord.utils import get
import youtube_dl
import os
from youtubesearchpython import Search


async def join(ctx, client):
    global voice
    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.author.voice.channel.connect()


async def leave(ctx, client):
    for voice_channel in client.voice_clients:
        if voice_channel.guild == ctx.guild:
            await voice_channel.disconnect()

queues = []


async def play(ctx, client, *url):
    voice = get(client.voice_clients, guild=ctx.guild)
    whole = ''
    for word in url:
        whole += word
    url = whole
    if voice == None or voice.is_connected() == False:
        await ctx.author.voice.channel.connect()

        voice = get(client.voice_clients, guild=ctx.guild)

    if os.path.isfile('song.mp3'):
        os.remove('song.mp3')
        queues.clear()

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except:
        allSearch = Search(url, limit=2)
        print(str(allSearch.result()))
        ur = "https://www.youtube.com/watch" + \
             (str(allSearch.result()).split("'link': 'https://www.youtube.com/watch"))[1].split("'")[0]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ur])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.0

    nname = name.rsplit('-', 1)
    embed = discord.Embed(title='Playing:', description=nname[0], color=0xfdf800)
    await ctx.send(embed=embed)


async def pause(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(title='Paused', color=0xfdf800)
    global embed_msg
    embed_msg = await ctx.send(embed=embed)
    voice.pause()


async def resume(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()
    await embed_msg.delete()


async def skip(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()


async def queue(ctx, url, client):
    if os.path.isdir('./Queue') is False:
        os.mkdir('Queue')
    q_num = len(os.listdir(os.path.abspath(os.path.realpath('Queue'))))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues.append(q_num)

    queue_path = os.path.abspath(os.path.realpath('Queue') + f'\song{q_num}.%(ext)s')

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    embed = discord.Embed(title='Queued:', color=0xfdf800)
    await ctx.send(embed=embed)