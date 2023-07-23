# -*- coding: utf-8 -*-
import os
import asyncio
from json import loads
import requests
import discord
from dotenv import load_dotenv

load_dotenv(verbose=True)


Token = os.getenv('Token')
Channel_ID_natural = int(os.getenv('Channel_ID_natural'))
Channel_ID_bangOn = int(os.getenv('Channel_ID_bangOn'))

twicth_Client_ID = os.getenv('twicth_Client_ID')
twitch_Secert_Key = os.getenv('twitch_Secert_Key')

Aka_ID = 'rh_ryu'
ment = '나 보러 안올거야?'
offline = '나 보고싶어? 나 대신 류튜브 봐줘!! 많관부!'
AkaName = ['아카이로 류', '류', '아카', '대장']


class MyClient(discord.Client):
    async def on_ready(self):
        channel_bangOn = self.get_channel(Channel_ID_bangOn)
        # await channel_natural.send('아카가 지구다, 세상이다, 최고다')
        # await channel_bangOn.send('똑똑히 봐라! 이게 아카다! 이게 아카이로 류다!')
        oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twicth_Client_ID +
                                  "&client_secret=" + twitch_Secert_Key + "&grant_type=client_credentials")
        access_token = loads(oauth_key.text)["access_token"]
        token_type = 'Bearer '
        authorization = token_type + access_token
        print(authorization)
        check = False
        while True:
            print("ready on Notification")
            # 트위치 api에게 방송 정보 요청
            headers = {'client-id': twicth_Client_ID,
                       'Authorization': authorization}
            response_channel = requests.get(
                'https://api.twitch.tv/helix/streams?user_login=' + Aka_ID, headers=headers)
            print(response_channel.text)
            # 라이브 상태 체크
            try:
                # 방송 정보에서 'data'에서 'type' 값이 live 이고 체크상태가 false 이면 방송 알림(오프라인이면 방송정보가 공백으로 옴)
                if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                    await channel_bangOn.send(ment + '\n' + loads(response_channel.text)['data'][0]['title'] + '\n https://www.twitch.tv/' + Aka_ID)
                    print("Online")
                    check = True
            except:
                print("Offline")
                check = False
            await asyncio.sleep(30)

    async def on_member_join(self, member):
        channel_natural = client.get_channel(Channel_ID_natural)
        print('여기 접속은 하니?')
        print(member)
        await channel_natural.send(f'{member.mention} 님, 류하 류하!')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content in ('안녕', '안녕하세요', '하이', 'hi', 'hello', '안뇽'):
            await message.channel.send('안녕, 너도 선타대야?')
        if any(word in message.content for word in AkaName) and '귀여워' in message.content:
            await message.channel.send('맞아, 옴총 귀여워🥰 아는구나?')
        if message.content in ('나도 친구', '친구하고 싶어요'):
            await message.channel.send('어.. 음.. 공룡.. 좋아하세요?')
        if any(word in message.content for word in AkaName) and '생일' and '언제' in message.content:
            await message.channel.send('그것도 몰라? 11월 1일이잖아!! 난 이런 게 서운해🥺')
        if any(word in message.content for word in ('보고싶다', '류튜브', '유튜브')):
            await message.channel.send(offline+'\n https://www.youtube.com/@ryuch.821')
        if message.content == '너 싫어':
            await message.channel.send('알빠노!')
        if message.content == '그거 알아?':
            await message.channel.send('몰?루')


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = MyClient(intents=intents)
client.run(Token)
