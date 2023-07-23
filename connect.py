import discord
from discord.ext import commands

Token = 'MTEzMjMyNTE5NTg1Njc0ODYxNA.Gh5ugU.5xbaLThIKP8JjlG0Bkqy2D9s1yrZ-yTF2Wf6uo'
Chnnel_ID = '1128273006830043156'


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
