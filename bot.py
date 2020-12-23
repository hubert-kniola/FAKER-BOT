import discord
import discord.utils
from discord.ext import commands
from datetime import date
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from discord.ext.commands import Bot
import asyncio

from discord.ext.commands import bot

TOKEN = 'NzkwODk5MjIyOTAyODY1OTIw.X-HUTA.zJRqa7qOlg_yhp0vGVLy1WNjOeo'

intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents=intent)


# def get_nsfw():
#    response = requests.get
#    ("https://scrolller.com/r/nsfw")
#    json_data = json.loads(response.)


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


def welcome_mess2(avatar):
    response = requests.get(avatar)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((428, 428), Image.ANTIALIAS)
    with Image.open(r'./background1.png', 'r') as background:
        with Image.new("L", img.size, 0) as mask:
            img_w, img_h = img.size
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2, (bg_h - img_h) - 316)
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
        await client.change_presence(activity=discord.Game(name=f'Aktualnie na {str(len(client.servers))} serwerach'))
        await asyncio.sleep(10)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #await client.change_presence(activity=discord.Game(name="jebanie Dainamo"))

    if message.content.startswith('!info'):
        msg = '**Witaj** {0.author.mention}\n Jestem botem stworzonym przez administrację serwera by stanowić ' \
              'autorski zamiennik na innego rodzaju boty!\n *W razie pytań zgłoś się do administracji*\n\n\n'.format(
            message)
        datex = f"{date.today().strftime('%d.%m.%Y')}"
        embed = discord.Embed(title='Hello!', description=msg, color=0xfdf800)
        embed.set_thumbnail(url= client.user.avatar_url)
        embed.add_field(name= '***BOT developed by FAKERS***', value=datex, inline=False)
        await message.channel.send(embed=embed)

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!powaga'):
        await message.channel.send("<:powaga:789143924760903751>")

    if message.content.startswith('!JD'):
        msg = 'Jebać {0.author.mention}'.format(message)
        await message.channel.send(msg)

    if message.content.startswith('!Dupa'):
        await message.channel.send("<:happy:789143635093880862>")

    if message.content.startswith('!image'):
        with open('image.jpg', 'rb') as image:
            await message.channel.send(file=discord.File(image, 'image.jpg'))

    if message.content.startswith('!msgId'):
        msg = '<@214056552217182209>\n' \
              'r u c h a n i e\n' \
              'sex'
        await message.channel.send(msg)

    if message.content.startswith('!halo'):
        author = message.author
        await message.channel.send(author.avatar_url)

    if message.content.startswith('!test'):
        channel = client.get_channel(790897876192591923)
        author = message.author
        welcome_mess(author.avatar_url)
        with open('welcome.png', 'rb') as welcome:
            await message.channel.send(file=discord.File(filename='welcome.png', fp=welcome))


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
