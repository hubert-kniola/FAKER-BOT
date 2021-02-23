import discord
import requests
import asyncio
import music
import quiz

from discord.ext import commands
from datetime import date
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO


token_file = open('TOKEN.txt')
TOKEN = token_file.read()

INTENT = discord.Intents.default()
INTENT.members = True
# client = discord.Client(intents=intent)
CLIENT = commands.Bot(command_prefix='!', intents=INTENT)
COLOR = 0x00f0fa

RES_PATH = {
    'bg': r'./res/background.png',
    'bg1': r'./res/background1.png',
    'bg2': r'./res/background2.png',
    'welcome': r'./res/welcome.png',
    'font': r'./res/RubikOne-Regular.ttf',
}

EMOTES = {
    'powaga': r'<:powaga:789143924760903751>',
}

ROLES = {
    'dj': r'» DJ',
}


def welcome_mess(author):
    response = requests.get(author.avatar_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((440, 440), Image.ANTIALIAS)
    text = 'Hello  ' + author.display_name

    with Image.open(RES_PATH['bg2'], 'r') as background:
        with Image.new("L", img.size, 0) as mask:
            img_w, img_h = img.size
            bg_w, bg_h = background.size
            offset = ((bg_w - img_w) // 2 + 8, (bg_h - img_h) - 212)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([(0, 0), img.size], fill=255)
            background.paste(img, offset, mask=mask)
            font = ImageFont.truetype(RES_PATH['font'], 100)
            draw = ImageDraw.Draw(background)
            txt_w, txt_h = draw.textsize(text, font=font)
            text_offset = (bg_w - txt_w) / 2, bg_h - 150
            bold = 4
            draw.text((text_offset[0] - bold, text_offset[1] -
                       bold), text, font=font, fill=(0, 0, 0))
            draw.text((text_offset[0] + bold, text_offset[1] -
                       bold), text, font=font, fill=(0, 0, 0))
            draw.text((text_offset[0] - bold, text_offset[1] +
                       bold), text, font=font, fill=(0, 0, 0))
            draw.text((text_offset[0] + bold, text_offset[1] +
                       bold), text, font=font, fill=(0, 0, 0))
            draw.text(text_offset, text, (255, 255, 255), font=font)

    background.resize((400, 195))
    background.save(RES_PATH['welcome'])


@CLIENT.event
async def status_task():
    while True:
        await CLIENT.change_presence(activity=discord.Streaming(name="Jebanie Dainamo", url='https://www.twitch.tv/dainamovsky'))
        await asyncio.sleep(60)
        await CLIENT.change_presence(activity=discord.Game(name=f'Aktualnie na {len(CLIENT.guilds)} serwerach'))
        await asyncio.sleep(60)
        await CLIENT.change_presence(activity=discord.Game(name='Czuwanie'))
        await asyncio.sleep(60)


@CLIENT.command()
async def info(ctx):
    msg = f'**Witaj** {ctx.author.mention}\n Jestem botem stworzonym przez administrację serwera by stanowić ' \
          'autorski zamiennik na innego rodzaju boty!\n *W razie pytań zgłoś się do administracji*\n\n\n'
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=COLOR)
    embed.set_thumbnail(url=CLIENT.user.avatar_url)
    embed.add_field(name='***BOT developed by FAKERS***',
                    value=datex, inline=False)
    await ctx.channel.send(embed=embed)


@CLIENT.command()
async def command(ctx):
    msg = f'**Witaj** {ctx.author.mention}\n Stosuj przedrostek !.\nOto wszystkie niezbędne komendy:\n\n----| GENERAL |----\n - !hello\n - !info\n - !powaga\n - !JD' \
          f'\n - !spam\n - !DM\n----| MUSIC |----\n - !join\n - !skip\n - !leave\n - !queue\n - !pause\n - !resume\n\n*W razie pytań zgłoś się do administracji*\n\n\n'
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=COLOR)
    embed.set_thumbnail(url=CLIENT.user.avatar_url)
    embed.add_field(name='***BOT developed by FAKERS***',
                    value=datex, inline=False)
    await ctx.channel.send(embed=embed)


@CLIENT.command()
async def hello(ctx):
    msg = f'Hello {ctx.author.mention}'
    await ctx.channel.send(msg)


@CLIENT.command()
async def powaga(ctx):
    await ctx.channel.send(EMOTES['powaga'])


@CLIENT.command()
async def JD(ctx):
    msg = f'Jebać {ctx.author.mention}'
    await ctx.channel.send(msg)


@CLIENT.command()
async def halo(ctx):
    await ctx.channel.send(ctx.author.avatar_url)


@CLIENT.command()
async def spam(ctx, msg):
    for i in range(10):
        await ctx.send(msg)


@CLIENT.command()
async def test(ctx):
    author = ctx.author
    welcome_mess(author)
    with open(RES_PATH['welcome'], 'r+b') as welcome:
        await ctx.channel.send(file=discord.File(filename=RES_PATH['welcome'], fp=welcome))


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def join(ctx):
    await music.join(ctx, CLIENT)


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def leave(ctx):
    await music.leave(ctx, CLIENT)


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def play(ctx, *url):
    await music.play(ctx, CLIENT, *url)


queues = []


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def queue(ctx, url):
    await music.queue(ctx, url, CLIENT)


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def pause(ctx):
    await music.pause(ctx, CLIENT)


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def resume(ctx):
    await music.resume(ctx, CLIENT)


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def skip(ctx):
    await music.skip(ctx, CLIENT)


async def private_welcome_message(member):
    user = CLIENT.get_user(member.id)
    msg = 'Witamy na serwerze FAKERS!\n' \
          'Życzymy miłego pobytu.\n' \
          'W razie problemów skorzystaj z komendy !help\n'
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=COLOR)
    embed.add_field(name='***BOT developed by FAKERS***',
                    value=datex, inline=False)
    await user.send(embed=embed)


@CLIENT.event
async def on_member_join(member):
    channel = CLIENT.get_channel(784084663593205820)
    msg = f"{member.mention} jesteś {member.guild.member_count} użytkownikiem naszego serwera!" \
          f"\n" \
          f"\n" \
        # f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=COLOR)
    await member.add_roles(discord.utils.get(member.guild.roles, name='» Essa'))
    await channel.send(embed=embed)
    author = member
    welcome_mess(author)

    with open(RES_PATH['welcome'], 'r+b') as welcome:
        await channel.send(file=discord.File(filename=RES_PATH['welcome'], fp=welcome))
    await private_welcome_message(member)


@CLIENT.event
async def on_member_remove(member):
    channel = CLIENT.get_channel(784084663593205820)
    msg = f"{member.mention} opuścił nas!" \
          f"\n" \
          f"\n" \
          f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Upsss!', description=msg, color=COLOR)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


@CLIENT.command()
async def DM(ctx, msg):
    msgr = f'Powiadomiono administrację'
    await ctx.channel.send(msgr)
    admins = 214056552217182209, 229147897378111488
    for userID in admins:
        user = CLIENT.get_user(userID)
        await user.send(msg)


@CLIENT.command()
@commands.has_role('»  Admin')
async def poke(ctx, Id, msg):
    user = CLIENT.get_user(int(Id))
    msgr = f'Wysłano'
    # await ctx.channel.send(msgr)
    await user.send(msg)


@CLIENT.command()
@commands.has_role('»  Admin')
async def emote(ctx):
    msg = '<:DJ:813410735283634206> - ranga » DJ\n' \
          '<:iman:813412758544056360> - ranga » Przyjęty\n' \
          '<:iwoman:813411955456475177> - ranga » Przyjęta\n' \
          '<:iheli:813413958207143966> - ranga » Helikopter\n' \
          '<:irocket:813417496311758870> - ranga » Rocket League\n' \
          '<:ilol:813416901924356117> - ranga » League of Legends'
    embed = discord.Embed(
        title='Zareaguj aby otrzymać rangę!', description=msg, color=COLOR)
    channel = CLIENT.get_channel(790897876192591923)
    message = await ctx.channel.send(embed=embed)
    await discord.Message.add_reaction(message, emoji=':DJ:813410735283634206')
    await discord.Message.add_reaction(message, emoji=':iman:813412758544056360')
    await discord.Message.add_reaction(message, emoji=':iwoman:813411955456475177')
    await discord.Message.add_reaction(message, emoji=':iheli:813413958207143966')
    await discord.Message.add_reaction(message, emoji=':irocket:813417496311758870')
    await discord.Message.add_reaction(message, emoji=':ilol:813416901924356117')


@CLIENT.event
async def on_reaction_add(reaction, member):
    #channel = client.get_channel(790897876192591923)
    if reaction.message.channel.id != 813417981815947274:
        return
    if member.id == 790899222902865920:
        return
    if reaction.emoji.name == 'DJ':
        await member.add_roles(discord.utils.get(member.guild.roles, name=ROLES['dj']))
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
    if reaction.emoji.name == 'first':
        print('Hubert tu był')
        return 0
    if reaction.emoji.name == 'second':
        return 1
    if reaction.emoji.name == 'third':
        return 2
    if reaction.emoji.name == 'fourth':
        return 3
    if reaction.emoji.name == 'fifth':
        return 4


@CLIENT.command()
async def emb(ctx, tit, *msg):
    whole = ''
    for word in msg:
        whole += ' ' + word
    msg = whole
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title=tit, description=msg, color=COLOR)
    embed.add_field(name='***BOT developed by FAKERS***',
                    value=datex, inline=False)
    await ctx.channel.send(embed=embed)


@CLIENT.command()
async def gifi(ctx):
    with open('fakers.gif', 'r+b') as gifi:
        await ctx.channel.send(file=discord.File(filename='fakers.gif', fp=gifi))


@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    CLIENT.loop.create_task(status_task())
    print('------')


# QUIZ COMMANDS

QUIZ = None

@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def qstart(ctx, *args):
    global QUIZ
    if QUIZ or len(args) != 4:
        await ctx.message.delete()
        return

    name, qtype, song_count, playlist = args
    qtype = quiz.QuizTypeEnum.RACE if qtype.lower() == 'race' else quiz.QuizTypeEnum.STD

    try:
        song_count = int(song_count)
    except Exception:
        await ctx.message.delete()
        return

    QUIZ = quiz.Quiz(qtype, name, playlist, song_count)

    await ctx.channel.send(f'Starting quiz: {QUIZ}\nRounds left: {QUIZ.songs_left}')


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def qstop(ctx):
    global QUIZ
    if not QUIZ:
        await ctx.message.delete()
        return

    await ctx.channel.send(f'Quiz finished.\nResults:\n{[(i, v) for i, v in QUIZ.summary()]}')

    QUIZ = None


@CLIENT.command()
async def qaddme(ctx):
    global QUIZ
    await ctx.message.delete()

    if not QUIZ:
        return

    name = ctx.author.display_name
    QUIZ.add_participant(quiz.Participant(name))

    await ctx.channel.send(f'{name} joined quiz {QUIZ}')


@CLIENT.command()
async def qvote(ctx, *args):
    global QUIZ
    if not QUIZ:
        await ctx.message.delete()
        return

    title = ' '.join(args)

###

CLIENT.run(TOKEN)
