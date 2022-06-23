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
    rollModifier = 0
    sum = 0
    modifier = False
    rollCommand = arg.split("d", 1)
    if '+' in arg:
        rollModifier = arg.split("+",1)
        print(str(rollModifier[0]) + '\t' + str(rollModifier[1]))
        rollCommand = rollModifier[0].split("d", 1)
        modifier = True
        sum = int(rollModifier[1])

    rollInstance = random.randint(1,int(rollCommand[1]))
    rollResults = [rollInstance]
    result = arg + ': ' + str(rollInstance)
    sum += rollInstance
    index = 1
    if int(rollCommand[0]) >= 10 or int(rollCommand[0]) <= 0:
        await ctx.send("no")
    else:
        while index < int(rollCommand[0]):
            rollInstance = random.randint(1,int(rollCommand[1]))
            rollResults.append(str(rollInstance))
            index += 1
            sum += rollInstance
            result = result + ' + ' + str(rollInstance)
        
        if modifier:
            if int(rollModifier[1]) < 0:
                result = result + ' - ' + str(rollModifier[1])
            elif int(rollModifier[1]) > 0:
                result = result + ' + ' + str(rollModifier[1])
        
        result = result + ' = ' + str(sum)
        print(result)
        await ctx.send(result)#',  '.join(rollResults))

# Run the bot
client.run(TOKEN)