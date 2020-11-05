import discord
import os
import re
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
ME = os.getenv('DISCORD_BOT_USERNAME')
client = discord.Client()

def extractFactorial(text):
    regex = '((|[0-9])[0-9])!'
    return re.findall(regex, text)

def doFactorial(num):
    if num > 1:
        return num * doFactorial(num-1)
    else:
        return num

def extractFibonacci(text):
    regex = 'fibonacci (([0-9][0-9]|[0-9]))'
    return re.findall(regex, text.lower())

def getFibonacci(num):
    if num <= 1:
        return num
    else:
        return (getFibonacci(num - 1) + getFibonacci(num - 2))

@client.event
async def on_ready():
    print(f'{client.user} connected to Discord!\n')

    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following server:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    channels = '\n - '.join([channel.name for channel in guild.channels])
    print(f'Server Channels:\n - {channels}')
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Server Members:\n - {members}')

@client.event
async def on_message(message):
    if str(message.channel) == 'dbratssandbox' and str(message.author) != ME:
        print(f'{message.author} sent a message on {message.channel}: {message.content}\n')
        res = await message.add_reaction('❤️')
        if res:
            print(f'Reaction was added to the message.')

        factorial = extractFactorial(message.content)
        if len(factorial) > 0:
            for f in factorial:
                num = int(f[0])
                fact = doFactorial(num)
                await message.channel.send(f'{f[0]}! is {fact}')

        fibonacci = extractFibonacci(message.content)
        if len(fibonacci) > 0:
            fibnums = list()
            for i in range(int(fibonacci[0][0])):
                fibnums.append(getFibonacci(i))

            fibresult = str(fibnums).replace('[', '').replace(']', '')
            await message.channel.send(f'Fibonacci: {fibresult}')

client.run(TOKEN)