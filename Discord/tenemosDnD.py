# Imports
import discord
from discord.ext import commands
import random
import re

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
    print("Original arg: " + str(arg))
    
    # Get die roll amount
    rollCommand = arg.split("d",1)
    rollCount = int(rollCommand[0])
    if rollCount >= 10 or rollCount <= 0:
        await ctx.send("no")
    print("RollCount: " + str(rollCount))
    
    # Get die roll value and modifier sum
    rollDie = 0
    modifierSum = 0
    if '+' or '-' in rollCommand[1]:
        modifierSum = eval(rollCommand[1])
        rollCommand = re.split('\+|\-',rollCommand[1])
        rollDie = rollCommand[0]
        modifierSum -= int(rollDie)
        print(str(modifierSum))
        print("RollDieA: " + str(rollDie))
    else:
        rollDie = rollCommand[1]
        print("RollDieB: " + str(rollDie))
    
    # Get roll sum
    rollSum = random.randint(1,int(rollDie))
    result = arg + ':\n' + str(rollSum)
    while rollCount > 1:
        randomRoll = random.randint(1,int(rollDie))
        result += ' + ' + str(randomRoll)
        rollSum += randomRoll
        rollCount -= 1
    
    # Get roll amount + modifiers
    totalSum = rollSum + modifierSum
    result += ' + modifiers ' + ' = ' + str(totalSum)
    await ctx.send(result)

    print("Done!")

# Run the bot
client.run(TOKEN)