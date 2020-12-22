import discord
from discord.ext import commands
from datetime import date

TOKEN = ''

intent = discord.Intents.default()
intent.members = True
client = discord.Client(intents=intent)


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

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


@client.event
async def on_member_join(member):
    channel = client.get_channel(790897876192591923)
    msg = f"{member.mention} jesteś {member.guild.member_count} użytkownikiem naszego serwera!" \
          f"\n" \
          f"\n" \
          f"{date.today().strftime('%d/%m/%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0x00ff00)
    await channel.send(embed=embed)


@client.event
async def on_member_remove(member):
    channel = client.get_channel(790897876192591923)
    msg = f"{member.mention} opuścił nas!" \
          f"\n" \
          f"\n" \
          f"{date.today().strftime('%d/%m/%Y')}"
    embed = discord.Embed(title='Hello!', description=msg, color=0xff0000)
    await channel.send(embed=embed)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
