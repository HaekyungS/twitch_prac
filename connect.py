# -*- coding: utf-8 -*-
import os
import asyncio
from json import loads
import requests
import discord
from dotenv import load_dotenv

# dotenv 사용을 위해, env를 읽는다.
load_dotenv(verbose=True)

# env에 담아둔 토큰값을 변수에 할당
Token = os.getenv('Token')
# Channel_ID_natural = int(os.getenv('Channel_ID_natural'))
# Channel_ID_bangOn = int(os.getenv('Channel_ID_bangOn'))

# 트위치 개발자 아이디와 시크릿키도 할당한다.
twicth_Client_ID = os.getenv('twicth_Client_ID')
twitch_Secert_Key = os.getenv('twitch_Secert_Key')

# 원하는 스트리머의 아이디.
Aka_ID = 'rh_ryu'

# 방송이 켜졌을 때, 링크와 함께 할 멘트
ment = '나 보러 안 올거야?'

# 다른 부분의 멘트
offline = '나 보고싶어? 나 대신 류튜브 봐줘!! 많관부!'

# 다양한 이름이라 배열로 담았다.
AkaName = ['아카이로 류', '류', '아카', '대장']


class MyClient(discord.Client):

    async def on_ready(self):
        # channel_bangOn = self.get_channel(Channel_ID_bangOn)

        for gulid in self.guilds:
            system_channel = gulid.system_channel
            if system_channel:
                await system_channel.send('안녕? 나는 아카이로 류님의 방송챗봇이야. 방송이 켜지면 내가 알려줄게!')

        # await channel_bangOn.send('안녕? 나는 아카이로 류님의 방송챗봇이야. 방송이 켜지면 내가 알려줄게!')

        # API 인증키 부분.
        oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twicth_Client_ID +
                                  "&client_secret=" + twitch_Secert_Key + "&grant_type=client_credentials")
        # access token
        access_token = loads(oauth_key.text)["access_token"]
        # 토큰 타입
        token_type = 'Bearer '
        # 서명
        authorization = token_type + access_token

        # print(authorization)

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
                    for guild in self.guilds:
                        system_channel = guild.system_channel
                        if system_channel:
                            await system_channel.send(ment + '\n' + loads(response_channel.text)['data'][0]['title'] + '\n https://www.twitch.tv/' + Aka_ID)
                    print("Online")
                    check = True
            except:
                print("Offline")
                check = False
            # 30초마다 요청을 보낸다.
            await asyncio.sleep(30)

    # 새로운 멤버가 접속하였을 때
    async def on_member_join(self, member):
        # 접속된 채널을 변수에 담는다.
        # channel_natural = client.get_channel(channel_natural)

        # 채널에 접속한 멤버를 언급하여 인사를 보낸다.
        await member.guild.system_channel.send(f'{member.mention} 님, 류하 류하!')

    # 특정 메세지에 대한 답변 설정
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
