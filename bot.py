import discord
from discord.ext import commands

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




@client.event
async def on_member_join(member):
    channel = client.get_channel(790897876192591923)
    print(f'{member.mention} joined!')
    await channel.send('hello')


@client.event
async def on_member_remove(member):
    channel = client.get_channel(790897876192591923)
    await channel.send('hello')

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
