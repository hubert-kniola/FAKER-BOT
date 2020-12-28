import discord
import discord.utils
from discord.utils import get
from discord.ext import commands
from datetime import date
import requests
from PIL import Image, ImageDraw
from io import BytesIO
import asyncio
import youtube_dl
import os
import shutil
from os import system
from youtubesearchpython import Search

token_file = open('TOKEN.txt')
TOKEN = token_file.read()

intent = discord.Intents.default()
intent.members = True
# client = discord.Client(intents=intent)
client = commands.Bot(command_prefix='!', intents=intent)


def welcome_mess(avatar):
    response = requests.get(avatar)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((435, 435), Image.ANTIALIAS)
    with Image.open(r'./background2.png', 'r') as background:
        with Image.new("L", img.size, 0) as mask:
            img_w, img_h = img.size
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2 + 8, (bg_h - img_h) - 214)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([(0, 0), img.size], fill=255)
            background.paste(img, offset, mask=mask)
    background.resize((400, 195))
    background.save('welcome.png')


@client.event
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name='Jebanie Dainamo'))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game(name=f'Aktualnie na {len(client.guilds)} serwerach'))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Game(name='Czuwanie'))
        await asyncio.sleep(60)


@client.command()
async def info(ctx):
    msg = f'**Witaj** {ctx.author.mention}\n Jestem botem stworzonym przez administrację serwera by stanowić ' \
          'autorski zamiennik na innego rodzaju boty!\n *W razie pytań zgłoś się do administracji*\n\n\n'
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0xfdf800)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name='***BOT developed by FAKERS***', value=datex, inline=False)
    await ctx.channel.send(embed=embed)


@client.command()
async def command(ctx):
    msg = f'**Witaj** {ctx.author.mention}\n Stosuj przedrostek !.\nOto wszystkie niezbędne komendy:\n - !hello\n - !powaga\n - !JD\n\n*W razie pytań zgłoś się do administracji*\n\n\n'
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0xfdf800)
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name='***BOT developed by FAKERS***', value=datex, inline=False)
    await ctx.channel.send(embed=embed)


@client.command()
async def hello(ctx):
    msg = f'Hello {ctx.author.mention}'
    await ctx.channel.send(msg)


@client.command()
async def powaga(ctx):
    await ctx.channel.send("<:powaga:789143924760903751>")


@client.command()
async def JD(ctx):
    msg = f'Jebać {ctx.author.mention}'
    await ctx.channel.send(msg)


@client.command()
async def halo(ctx):
    await ctx.channel.send(ctx.author.avatar_url)


@client.command()
async def task(ctx, zadanie):
    embed = discord.Embed(title=zadanie, color=0xfdf800)
    await ctx.send(embed=embed)


@client.command()
async def spam(ctx, msg):
    for i in range(10):
        await ctx.send(msg)


@client.command()
async def test(ctx):
    author = ctx.author
    welcome_mess(author.avatar_url)
    with open('welcome.png', 'rb') as welcome:
        await ctx.channel.send(file=discord.File(filename='welcome.png', fp=welcome))


@client.command()
@commands.has_role('» DJ')
async def join(ctx):
    global voice
    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.author.voice.channel.connect()


@client.command()
@commands.has_role('» DJ')
async def leave(ctx):
    for voice_channel in client.voice_clients:
        if voice_channel.guild == ctx.guild:
            await voice_channel.disconnect()


@client.command()
@commands.has_role('» DJ')
async def play(ctx, *url):
    async def check_queue():
        if os.path.isdir('./Queue') is True:
            DIR = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(DIR))
            try:
                first_file = os.listdir(DIR)[0]
            except:
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                if os.path.isfile('song.mp3'):
                    os.remove('song.mp3')
                shutil.move(song_path, main_location)
                for file in os.listdir('./'):
                    if file.endswith('.mp3'):
                        name = file
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 1.0

                nname = name.rsplit('-', 1)
                embed = discord.Embed(title='Playing:', description=nname[0], color=0xfdf800)
                await ctx.send(embed=embed)

            else:
                queues.clear()
                return

    voice = get(client.voice_clients, guild=ctx.guild)
    whole = ''
    for word in url:
        whole += word
    url = whole
    if voice == None or voice.is_connected() == False:
        await ctx.author.voice.channel.connect()

        Queue_infile = os.path.isdir('./Queue')
        try:
            Queue_folder = './Queue'
            if Queue_infile is True:
                print()
                shutil.rmtree(Queue_folder)
        except:
            print()

        voice = get(client.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        await queue(ctx, url)
        return

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
        allSearch = Search(url, limit=1)
        ur = "https://www.youtube.com/watch" + (str(allSearch.result()).split("'link': 'https://www.youtube.com/watch"))[1].split("'")[0]
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([ur])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 1.0

    nname = name.rsplit('-', 1)
    embed = discord.Embed(title='Playing:', description=nname[0], color=0xfdf800)
    await ctx.send(embed=embed)


queues = []


@client.command()
@commands.has_role('» DJ')
async def queue(ctx, url):
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


@client.command()
@commands.has_role('» DJ')
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    embed = discord.Embed(title='Paused', color=0xfdf800)
    global embed_msg
    embed_msg = await ctx.send(embed=embed)
    voice.pause()


@client.command()
@commands.has_role('» DJ')
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()
    await embed_msg.delete()


@client.command()
@commands.has_role('» DJ')
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()


@client.event
async def on_member_join(member):
    channel = client.get_channel(790897876192591923)
    msg = f"{member.mention} jesteś {member.guild.member_count} użytkownikiem naszego serwera! {member.avatar_url}" \
          f"\n" \
          f"\n" \
          f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0xfdf800)
    embed.set_thumbnail(url=member.avatar_url)
    await member.add_roles(discord.utils.get(member.guild.roles, name='Essa'))
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    channel = client.get_channel(790897876192591923)
    msg = f"{member.mention} opuścił nas!" \
          f"\n" \
          f"\n" \
          f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0xff0000)
    await channel.send(embed=embed)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    client.loop.create_task(status_task())
    print('------')


client.run(TOKEN)
