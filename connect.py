import discord
from discord.ext import commands

Token = '토큰'
Chnnel_ID = '채널아이디'


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(Token)
