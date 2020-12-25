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
        await client.change_presence(activity=discord.Game(name='jebanie Dainamo'))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game(name=f'Aktualnie na {len(client.guilds)} serwerach'))
        await asyncio.sleep(10)
        await client.change_presence(activity=discord.Game(name='czuwanie'))
        await asyncio.sleep(10)


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
async def test(ctx):
    author = ctx.author
    welcome_mess(author.avatar_url)
    with open('welcome.png', 'rb') as welcome:
        await ctx.channel.send(file=discord.File(filename='welcome.png', fp=welcome))


@client.command()
async def join(ctx):
    global voice
    voice = get(client.voice_clients, guild=ctx.guild)
    await ctx.author.voice.channel.connect()


@client.command()
async def leave(ctx):
    for voice_channel in client.voice_clients:
        if voice_channel.guild == ctx.guild:
            await voice_channel.disconnect()


@client.command()
async def play(ctx, url):
    file_exists = os.path.isfile('song.mp3')
    if file_exists:
        os.remove('song.mp3')
    voice = get(client.voice_clients, guild=ctx.guild)
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

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.1

    nname = name.rsplit('-', 2)
    await ctx.send(f'Playing: {nname[0]} - {nname[1]}')

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
