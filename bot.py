import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from findnamescog import checkNextBatch

load_dotenv()
TOKEN = os.getenv('DISCORD_CLIENT_SECRET')
GUILD = os.getenv('DISCORD_GUILD')
ME = os.getenv('DISCORD_BOT_USERNAME')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} connected to Discord!\n')
    checkNextBatch.start(client)

    print(
        f'{client.user} is connected to the following server:')
    for g in client.guilds:
        print(
            f'{g.name}(id: {g.id})\n'
        )

    guild = client.guilds[0]
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

if __name__ == '__main__':
    client.run(TOKEN)
