from os import name
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
    'gif': r'./res/fakers.gif',
}

EMOTES = {
    'powaga': r'<:powaga:789143924760903751>',
}

ROLES = {
    'dj': r'» DJ',
    'quizer': r'» Quizer',
    'admin': r'»  Admin',
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
        await CLIENT.change_presence(
            activity=discord.Streaming(name="Jebanie Dainamo", url='https://www.twitch.tv/dainamovsky'))
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
                    value=datex + ' ©️', inline=False)
    await ctx.channel.send(embed=embed)


@CLIENT.command()
async def command(ctx):
    msg = f'**Witaj** {ctx.author.mention}\n Stosuj przedrostek !.\nOto wszystkie niezbędne komendy:\n\n---- GENERAL ' \
          f'----\n - !hello\n - !info\n - !powaga\n - !JD' \
          f'\n - !spam\n - !DM\n---- MUSIC ----\n - !join\n - !skip\n - !leave\n - !queue\n - !pause\n - !resume\n' \
          f'--- QUIZY ---\n - !qstart\n - !qstop\n - !qjoin\n - !qround\n\n*W razie pytań zgłoś się do ' \
          f'administracji*\n\n\n '
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
    await ctx.message.delete()


@CLIENT.command()
async def JD(ctx):
    msg = f'Jebać {ctx.author.mention}'
    await ctx.channel.send(msg)
    await ctx.message.delete()


@CLIENT.command()
async def halo(ctx):
    await ctx.channel.send(ctx.author.avatar_url)
    await ctx.message.delete()


@CLIENT.command()
async def spam(ctx, msg):
    await ctx.message.delete()
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
    await music.queue(ctx, url)


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
          'W razie problemów skorzystaj z komendy !info oraz !command\n'
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=COLOR)
    embed.add_field(name='***BOT developed by FAKERS***',
                    value=datex + '©️', inline=False)
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
@commands.has_role(ROLES['admin'])
async def poke(ctx, Id, *msg):
    await ctx.message.delete()
    whole = ''
    for word in msg:
        whole += ' ' + word
    msg = whole
    user = CLIENT.get_user(int(Id))
    msgr = f'Wysłano'
    await ctx.channel.send(msgr)
    await user.send(msg)


@CLIENT.command()
@commands.has_role('»  Admin')
async def emote(ctx):
    msg = '<:DJ:813410735283634206> - ranga » DJ\n' \
          '<:iman:813412758544056360> - ranga » Przyjęty\n' \
          '<:iwoman:813411955456475177> - ranga » Przyjęta\n' \
          '<:iheli:813413958207143966> - ranga » Helikopter\n' \
          '<:irocket:813417496311758870> - ranga » Rocket League\n' \
          '<:ilol:813416901924356117> - ranga » League of Legends\n' \
          '<:imango:814168091109097503> - ranga » Quizer\n' \
          '<:ibdo1:814502384084320329> - ranga » Black Desert\n' \
          '<:iterraria:814502455651205120> - ranga » Terraria\n' \
          '<:igta:814502239103221770> - ranga » GTA V'
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
    await discord.Message.add_reaction(message, emoji=':imango:814168091109097503')
    await discord.Message.add_reaction(message, emoji=':ibdo1:814502384084320329')
    await discord.Message.add_reaction(message, emoji=':iterraria:814502455651205120')
    await discord.Message.add_reaction(message, emoji=':igta:814502239103221770')


@CLIENT.event
async def on_reaction_add(reaction, member):
    # channel = client.get_channel(790897876192591923)
    # if reaction.message.channel.id != 813417981815947274:
    #    return
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
    if reaction.emoji.name == 'imango':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Quizer'))
    if reaction.emoji.name == 'ibdo1':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Black Desert'))
    if reaction.emoji.name == 'iterraria':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» Terraria'))
    if reaction.emoji.name == 'igta':
        await member.add_roles(discord.utils.get(member.guild.roles, name='» GTA V'))
    if reaction.emoji.name == 'ipause':
        await pause(reaction.message.channel)
    if reaction.emoji.name == 'iplay':
        await resume(reaction.message.channel)
    if reaction.emoji.name == 'iskip':
        await skip(reaction.message.channel)


@CLIENT.command()
@commands.has_role(ROLES['admin'])
async def emb(ctx, tit, *msg):
    whole = ''
    for word in msg:
        whole += ' ' + word
    msg = whole
    datex = f"{date.today().strftime('%d.%m.%Y')}"
    embed = discord.Embed(title=tit, description=msg, color=COLOR)
    embed.add_field(name='***BOT developed by FAKERS***', value=datex, inline=False)
    await ctx.channel.send(embed=embed)


@CLIENT.command()
@commands.has_role(ROLES['admin'])
async def gifi(ctx):
    with open(RES_PATH['gif'], 'r+b') as gifi:
        await ctx.channel.send(file=discord.File(filename='fakers.gif', fp=gifi))


@CLIENT.event
async def on_ready():
    print('Logged in as')
    print(CLIENT.user.name)
    print(CLIENT.user.id)
    CLIENT.loop.create_task(status_task())
    print('------')


# QUIZ COMMANDS

def info_embed(title, text='', footer=False):
    embed = discord.Embed(title=title,
                          description=text,
                          color=COLOR)
    if footer:
        embed.add_field(name='***BOT developed by FAKERS***',
                        value=f"{date.today().strftime('%d.%m.%Y')}", inline=False)
    return embed


QUIZ = None


@CLIENT.command()
@commands.has_role(ROLES['dj'])
async def qinfo(ctx):
    await ctx.channel.send(embed=info_embed("OP QUIZ Instruction", """
        - !qstart NAME ROUNDS_TO_PLAY (DIFFICULTY|MAL PROFILE NAME)
        - !qjoin
        - !qround TIME
        - !qv SOME ANIME TITLE
        - !qstop

        Disclaimer:
        - You need a rank to do quizes.
        - DIFFICULTY is an integer N which is multiplied 50 times. That numer is the pool of most popular anime from MAL used in game. Ca 8 is reasonable.
        - MAL PROFILE NAME allows to use a real person's anime list for playing.
        - TIME is the duration in seconds for which the tracks will play. Minimum is 5, maximum is 60.
        - You can vote only while the song is still playing.
        - Voting is done via DMs. You can vote on the starting channel but it will be visible to others.
        """, footer=True))


@CLIENT.command()
@commands.has_role(ROLES['quizer'])
async def qstart(ctx, *args):
    global QUIZ
    await ctx.message.delete()

    if not QUIZ and len(args) == 3:
        name, song_count, diff_or_name = args
    else:
        return

    try:
        song_count = int(song_count)
    except Exception:
        await ctx.message.delete()
        return

    try:
        difficulty = int(diff_or_name)
        QUIZ = quiz.Quiz(name, song_count, difficulty, ctx.channel)

    except Exception:
        QUIZ = quiz.Quiz(name, song_count, 1, ctx.channel)
        QUIZ.profile = diff_or_name

    msg = info_embed(f'Starting quiz: {QUIZ}', f"""
        {QUIZ.songs_left} rounds left. 
        """)

    await QUIZ.channel.send(embed=msg)
    await QUIZ.send_to_all(embed=msg)


@CLIENT.command()
@commands.has_role(ROLES['quizer'])
async def qstop(_ctx):
    global QUIZ
    if not QUIZ:
        return

    result_str = '\n'.join(
        [f'{i}. {entry[0]} - {entry[1]} points' for i, entry in QUIZ.summary()])
    actual_str = '\n'.join([f'{i}. {entry.titles[0]} or {entry.titles[1]} "{entry.element}"' for i,
                                                                                                 entry in
                            enumerate(QUIZ.entry_history, start=1)])
    votes_str = '\n\n'.join(
        [f'{p.name.capitalize()}\'s correct choices are {p.get_summary()[0]}, wrong are {p.get_summary()[1]}.' for p in
         QUIZ.participants])

    msg = info_embed(f'Quiz finished', f"""
    Results:
    {result_str}
    """, footer=True)

    await QUIZ.channel.send(embed=msg)
    await QUIZ.send_to_all(embed=msg)

    await QUIZ.channel.send(f"""
    Correct titles in order:
    {actual_str}
    """)

    await QUIZ.channel.send(f"""
    Participant's choices:
    {votes_str}
    """)

    QUIZ = None


@CLIENT.command()
@commands.has_role(ROLES['quizer'])
async def qjoin(ctx):
    global QUIZ
    await ctx.message.delete()

    if not QUIZ or QUIZ.has_started:
        return

    name = ctx.author.display_name
    QUIZ.add_participant(quiz.Participant(name, await ctx.author.create_dm()))

    msg = info_embed(f'{name} joined quiz {QUIZ}')
    await QUIZ.channel.send(embed=msg)
    await QUIZ.send_to_all(embed=msg)


@CLIENT.command()
@commands.has_role(ROLES['quizer'])
async def qround(ctx, timeout):
    global QUIZ
    await ctx.message.delete()

    if not QUIZ:
        return

    timeout = int(timeout)
    timeout = timeout if timeout > 5 and timeout < 60 else 60

    msg = info_embed(
        f'Round {QUIZ.round} will take {timeout} seconds.\n', 'Preparing...')
    await QUIZ.channel.send(embed=msg)
    await QUIZ.send_to_all(embed=msg)

    await QUIZ.new_entry()
    await music.quiz_play(ctx, CLIENT, QUIZ.current_entry.query())

    msg = info_embed(f'Round {QUIZ.round} starting now!')
    await QUIZ.channel.send(embed=msg)
    await QUIZ.send_to_all(embed=msg)

    await music.quiz_stop(ctx, CLIENT, timeout, QUIZ.send_to_all)

    msg = info_embed(
        f'It was {QUIZ.current_entry.element} from {QUIZ.current_entry.titles[0]} aka {QUIZ.current_entry.titles[1]}.\n',
        f'There are {QUIZ.songs_left} rounds left.')
    await QUIZ.channel.send(embed=msg)
    await QUIZ.send_to_all(embed=msg)

    if not QUIZ.next_round():
        await qstop(ctx)


@CLIENT.command()
async def qv(ctx, *args):
    global QUIZ

    if not QUIZ or not QUIZ.current_entry:
        return

    if ctx.channel == QUIZ.channel:
        await ctx.message.delete()

    name = ctx.author.display_name
    if QUIZ.is_participant(name):
        title = ' '.join(args)
        QUIZ.current_votes[name] = (title, QUIZ.current_entry.verify(title))

        await QUIZ.channel.send(embed=info_embed(f'{name} has voted'))
        await QUIZ.send_to_all(embed=info_embed(f'{name} has voted'))


#####

CLIENT.run(TOKEN)
