import asyncio
import discord
import youtube_dl
import os
import re
import asyncio

from discord.utils import get
from youtubesearchpython import Search

COLOR = 0x00f0fa
MUSIC_LIST = []


async def join(ctx, client):
    global voice
    MUSIC_LIST.clear()

    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.author.voice.channel.connect()
    await ctx.message.delete()


async def leave(ctx, client):
    for voice_channel in client.voice_clients:
        if voice_channel.guild == ctx.guild:
            await voice_channel.disconnect()
    await ctx.message.delete()


async def play(ctx, client, *url):
    await ctx.message.delete()
    MUSIC_LIST.clear()

    voice = get(client.voice_clients, guild=ctx.guild)

    url = ' '.join(url)

    if not voice or not voice.is_connected():
        await ctx.author.voice.channel.connect()
        voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': r'./song.webm',
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            entries = info['entries']
            for entry in entries:
                t = entry['title'], entry['webpage_url']
                MUSIC_LIST.append(t)
    except KeyError:
        t = info['title'], info['webpage_url']
        MUSIC_LIST.append(t)
    except:
        allSearch = Search(url, limit=5)
        print(str(allSearch.result()))
        list = re.findall(
            r'\bhttps://www\.youtube\.com/watch[^\']+\w+', str(allSearch.result()))
        print(list)
        list2 = re.findall(r'title\': \'[^\']+\w+.', str(allSearch.result()))
        list3 = []
        count = 0
        for e in list2:
            if count % 2 == 0:
                print(e)
                e = e.replace('title\': \'', '')
                list3.append(e)
            count += 1
        print(list3)

        msg = f'1. {list3[0]}\n' \
              f'2. {list3[1]}\n' \
              f'3. {list3[2]}\n' \
              f'4. {list3[3]}\n' \
              f'5. {list3[4]}'
        embed = discord.Embed(title='Wyniki wyszukiwania:',
                              description=msg, color=COLOR)
        message = await ctx.channel.send(embed=embed)
        await discord.Message.add_reaction(message, emoji=':first:813519059081232384')
        await discord.Message.add_reaction(message, emoji=':second:813519081697312819')
        await discord.Message.add_reaction(message, emoji=':third:813519093520924702')
        await discord.Message.add_reaction(message, emoji=':fourth:813519113354739783')
        await discord.Message.add_reaction(message, emoji=':fifth:813519124865089627')

        def _check(r, u):
            return (
                u == ctx.author
                and r.message.id == message.id
            )

        option, _ = await client.wait_for("reaction_add", timeout=60.0, check=_check)

        def switch(opt):
            return {
                'first': 0,
                'second': 1,
                'third': 2,
                'fourth': 3,
                'fifth': 4,
            }[opt]
        await message.delete()
        print(option.emoji.name)
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([list[switch(option.emoji.name)]])
            
        voice.play(discord.FFmpegPCMAudio('song.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1.0

        nname = name.rsplit('-', 1) # TODO: co to za zmienna 'name'?
        embed = discord.Embed(title='Odtwarzam:',
                              description=nname[0], color=COLOR)
        message = await ctx.send(embed=embed)

        await discord.Message.add_reaction(message, emoji=':ipause:813867984644866099')
        await discord.Message.add_reaction(message, emoji=':iplay:813867994903216208')
        await discord.Message.add_reaction(message, emoji=':iskip:813868004664017004')

        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1)

        os.remove('./song.mp3')

    for tr in MUSIC_LIST:
        ydl.download([tr[1]]) # TODO: skad to 'ydl'? to z linijki 119 już nie istnieje

        voice.play(discord.FFmpegPCMAudio('song.mp3'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1.0

        nname = name.rsplit('-', 1)
        embed = discord.Embed(title='Odtwarzam:',
                              description=nname[0], color=COLOR)
        message = await ctx.send(embed=embed)

        await discord.Message.add_reaction(message, emoji=':ipause:813867984644866099')
        await discord.Message.add_reaction(message, emoji=':iplay:813867994903216208')
        await discord.Message.add_reaction(message, emoji=':iskip:813868004664017004')
        while voice.is_playing() or voice.is_paused():
            await asyncio.sleep(1)

        os.remove('./song.mp3')


async def quiz_play(ctx, client, title):
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice or not voice.is_connected():
        await ctx.author.voice.channel.connect()
        voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': r'./quiz.webm',
    }

    search = Search(title, limit=1).result()
    link = search['result'][0]['link']

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

    voice.play(discord.FFmpegPCMAudio(r'./quiz.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.0


async def quiz_stop(ctx, client, timeout, send_delegate):
    await asyncio.sleep(timeout - 5)
    await send_delegate('5...')
    await asyncio.sleep(1)
    await send_delegate('4...')
    await asyncio.sleep(1)
    await send_delegate('3...')
    await asyncio.sleep(1)
    await send_delegate('2...')
    await asyncio.sleep(1)
    await send_delegate('1...')
    await asyncio.sleep(1)

    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()

    os.remove(r'./quiz.mp3')


async def pause(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(title='Wstrzymano', color=COLOR)
    global embed_msg
    embed_msg = await ctx.send(embed=embed)
    voice.pause()
    await ctx.message.delete()


async def resume(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()
    await embed_msg.delete()
    await ctx.message.delete()


async def skip(ctx, client):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and not voice.is_playing():
        await embed_msg.delete()
    if voice:
        voice.stop()
    await ctx.message.delete()


async def queue(ctx, url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    track = info['title'], info['webpage_url']
    MUSIC_LIST.append(track)
