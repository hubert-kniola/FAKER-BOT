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
from PIL import Image, ImageFont, ImageDraw
import music

token_file = open('TOKEN.txt')
TOKEN = token_file.read()

intent = discord.Intents.default()
intent.members = True
# client = discord.Client(intents=intent)
client = commands.Bot(command_prefix='!', intents=intent)


def welcome_mess(author):
    response = requests.get(author.avatar_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((440, 440), Image.ANTIALIAS)
    text = 'Hello  ' + author.display_name
    with Image.open(r'./background2.png', 'r') as background:
        with Image.new("L", img.size, 0) as mask:
            img_w, img_h = img.size
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2 + 8, (bg_h - img_h) - 212)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([(0, 0), img.size], fill=255)
            background.paste(img, offset, mask=mask)
            font = ImageFont.truetype('fonts/RubikOne-Regular.ttf', 100)
            draw = ImageDraw.Draw(background)
            txt_w, txt_h = draw.textsize(text, font=font)
            text_offset = (bg_w - txt_w) / 2, bg_h - 150
            bold = 4
            draw.text((text_offset[0] - bold, text_offset[1] - bold), text, font=font, fill=(0, 0, 0))
            draw.text((text_offset[0] + bold, text_offset[1] - bold), text, font=font, fill=(0, 0, 0))
            draw.text((text_offset[0] - bold, text_offset[1] + bold), text, font=font, fill=(0, 0, 0))
            draw.text((text_offset[0] + bold, text_offset[1] + bold), text, font=font, fill=(0, 0, 0))
            draw.text(text_offset, text, (255, 255, 255), font=font)
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
    msg = f'**Witaj** {ctx.author.mention}\n Stosuj przedrostek !.\nOto wszystkie niezbędne komendy:\n\n----| GENERAL |----\n - !hello\n - !info\n - !powaga\n - !JD' \
          f'\n - !spam\n - !DM\n----| MUSIC |----\n - !join\n - !skip\n - !leave\n - !queue\n - !pause\n - !resume\n\n*W razie pytań zgłoś się do administracji*\n\n\n'
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
async def spam(ctx, msg):
    for i in range(10):
        await ctx.send(msg)


@client.command()
async def test(ctx):
    author = ctx.author
    welcome_mess(author)
    with open('welcome.png', 'rb') as welcome:
        await ctx.channel.send(file=discord.File(filename='welcome.png', fp=welcome))


@client.command()
@commands.has_role('» DJ')
async def join(ctx):
    await music.join(ctx, client)


@client.command()
@commands.has_role('» DJ')
async def leave(ctx):
    await music.leave(ctx, client)


@client.command()
@commands.has_role('» DJ')
async def play(ctx, *url):
    await music.play(ctx, client, *url)


queues = []


@client.command()
@commands.has_role('» DJ')
async def queue(ctx, url):
    await music.queue(ctx, url, client)


@client.command()
@commands.has_role('» DJ')
async def pause(ctx):
    await music.pause(ctx, client)


@client.command()
@commands.has_role('» DJ')
async def resume(ctx):
    await music.resume(ctx, client)


@client.command()
@commands.has_role('» DJ')
async def skip(ctx):
    await music.skip(ctx, client)


async def private_welcome_message(member):
    user = client.get_user(member.id)
    msg = 'Witamy na serwerze FAKERS!\n' \
          'Życzymy miłego pobytu.\n' \
          'W razie problemów skorzystaj z komendy !help\n'
    embed = discord.Embed(title='Hello!', description=msg, color=0xfdf800)
    embed.add_field(name='***BOT developed by FAKERS***', value='', inline=False)
    await user.send(embed=embed)


@client.event
async def on_member_join(member):
    channel = client.get_channel(784084663593205820)
    msg = f"{member.mention} jesteś {member.guild.member_count} użytkownikiem naszego serwera!" \
          f"\n" \
          f"\n" \
        # f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0xfdf800)
    await member.add_roles(discord.utils.get(member.guild.roles, name='» Essa'))
    await channel.send(embed=embed)
    author = member
    welcome_mess(author)
    with open('welcome.png', 'rb') as welcome:
        await channel.send(file=discord.File(filename='welcome.png', fp=welcome))
    await private_welcome_message(member)


@client.event
async def on_member_remove(member):
    channel = client.get_channel(784084663593205820)
    msg = f"{member.mention} opuścił nas!" \
          f"\n" \
          f"\n" \
          f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Upsss!', description=msg, color=0xff0000)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


@client.command()
async def DM(ctx, msg):
    msgr = f'Powiadomiono administrację'
    await ctx.channel.send(msgr)
    admins = 214056552217182209, 229147897378111488
    for userID in admins:
        user = client.get_user(userID)
        await user.send(msg)


@client.command()
@commands.has_role('»  Admin')
async def poke(ctx, member, msg):
    user = client.get_user(member.id)
    msgr = f'Wysłano'
    await ctx.channel.send(msgr)
    await user.send(msg)


@client.command()
@commands.has_role('»  Admin')
async def emote(ctx):
    msg = '<:DJ:813410735283634206> - ranga » DJ\n' \
          '<:iman:813412758544056360> - ranga » Przyjęty\n' \
          '<:iwoman:813411955456475177> - ranga » Przyjęta\n' \
          '<:iheli:813413958207143966> - ranga » Helikopter\n' \
          '<:irocket:813417496311758870> - ranga » Rocket League\n' \
          '<:ilol:813416901924356117> - ranga » League of Legends'
    embed = discord.Embed(title='Zareaguj aby otrzymać rangę!', description=msg, color=0xfdf800)
    channel = client.get_channel(790897876192591923)
    message = await ctx.channel.send(embed=embed)
    await discord.Message.add_reaction(message, emoji=':DJ:813410735283634206')
    await discord.Message.add_reaction(message, emoji=':iman:813412758544056360')
    await discord.Message.add_reaction(message, emoji=':iwoman:813411955456475177')
    await discord.Message.add_reaction(message, emoji=':iheli:813413958207143966')
    await discord.Message.add_reaction(message, emoji=':irocket:813417496311758870')
    await discord.Message.add_reaction(message, emoji=':ilol:813416901924356117')


@client.event
async def on_reaction_add(reaction, member):
    #channel = client.get_channel(790897876192591923)
    if reaction.message.channel.id != 813417981815947274:
        return
    if member.id == 790899222902865920:
        return
    if reaction.emoji.name == 'DJ':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» DJ'))
    if reaction.emoji.name == 'iman':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Przyjęty'))
    if reaction.emoji.name == 'iwoman':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Przyjęta'))
    if reaction.emoji.name == 'iheli':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Helikopter'))
    if reaction.emoji.name == 'irocket':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Rocket League'))
    if reaction.emoji.name == 'ilol':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» League of Legends'))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    client.loop.create_task(status_task())
    print('------')


client.run(TOKEN)
