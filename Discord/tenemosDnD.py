# Imports
import discord
from discord.ext import commands
import random

# Credentials
f = open("token.txt", "r")
TOKEN = f.read()

# Create bot
client = commands.Bot(command_prefix='/')

# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))

# Command
@client.command()
async def weeb(ctx):
    await ctx.send('UwU')
@client.command()
async def r(ctx, arg):
    # WIP
    #rollCommand = ''
    #if '+' in arg:
    #    rollCommand = arg.split("+",1)

    rollCommand = arg.split("d", 1)
    rollResults = []
    index = 0
    if int(rollCommand[0]) >= 10 or int(rollCommand[0]) <= 0:
        await ctx.send("no")
    else:
        while index < int(rollCommand[0]):
            rollInstance = random.randint(1,int(rollCommand[1]))
            rollResults.append(str(rollInstance))
            index += 1
        await ctx.send(',  '.join(rollResults))

# Run the bot
client.run(TOKEN)