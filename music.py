import discord
import discord.utils
from discord.utils import get
import youtube_dl
import os
from youtubesearchpython import Search
import re

color = 0x00f0fa

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
        whole += word + ' '
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
        allSearch = Search(url, limit=5)
        print(str(allSearch.result()))
        list = re.findall(r'\bhttps://www\.youtube\.com/watch[^\']+\w+', str(allSearch.result()))
        print(list)
        list2 = re.findall(r'title\': \'[^\']+\w+.', str(allSearch.result()))
        list3 = []
        count = 0
        for e in list2:
            if count % 2 == 0:
                print(e)
                e = e.removeprefix('title\': \'')
                list3.append(e)
            count += 1
        print(list3)
        msg = f'1. {list3[0]}\n' \
              f'2. {list3[1]}\n' \
              f'3. {list3[2]}\n' \
              f'4. {list3[3]}\n' \
              f'5. {list3[4]}'
        embed = discord.Embed(title='Wyniki wyszukiwania:', description=msg, color=color)
        message = await ctx.channel.send(embed=embed)
        await discord.Message.add_reaction(message, emoji=':first:813519059081232384')
        await discord.Message.add_reaction(message, emoji=':second:813519081697312819')
        await discord.Message.add_reaction(message, emoji=':third:813519093520924702')
        await discord.Message.add_reaction(message, emoji=':fourth:813519113354739783')
        await discord.Message.add_reaction(message, emoji=':fifth:813519124865089627')

        def _check(r, u):
            return (
                u == ctx.author
                # dodać id wiadomości
            )

        option, _ = await client.wait_for("reaction_add", timeout=60.0, check=_check)
        def switch(opt):
            return{
                'first' : 0,
                'second' : 1,
                'third' : 2,
                'fourth' : 3,
                'fifth' : 4,
            }[opt]

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([list[switch(option.emoji.name)]])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.0

    nname = name.rsplit('-', 1)
    embed = discord.Embed(title='Playing:', description=nname[0], color=color)
    await ctx.send(embed=embed)


async def pause(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(title='Paused', color=color)
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
    embed = discord.Embed(title='Queued:', color=color)
    await ctx.send(embed=embed)