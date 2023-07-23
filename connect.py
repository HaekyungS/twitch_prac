# -*- coding: utf-8 -*-

import discord
import requests
from json import loads
import asyncio


Token = '내 토큰'
Channel_ID_natural = '내 채널'
Channel_ID_bangOn = '내 채널'

twicth_Client_ID = '채널 아이디'
twitch_Secert_Key = '비밀키'
Aka_ID = 'rh_ryu'
ment = '나 보러 안올거야?'
offline = '내가 보고 싶다면 류튜브 봐줘!!'

# channel_bangOn = discord.Client().get_channel(Channel_ID_bangOn)
# channel_natural = discord.Client().get_channel(Channel_ID_natural)


class MyClient(discord.Client):

    async def on_ready(self):
        channel_natural = self.get_channel(Channel_ID_natural)
        channel_bangOn = self.get_channel(Channel_ID_bangOn)

        await channel_natural.send('아카가 지구다, 세상이다, 최고다')
        await channel_bangOn.send('똑똑히 봐라! 이게 아카다! 이게 아카이로 류다!')

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
                    await channel_bangOn.send(ment + '\n https://www.twitch.tv/' + Aka_ID)
                    print("Online")
                    check = True

            except:
                # await channel_bangOn.send(offline+'\n https://www.youtube.com/@ryuch.821')
                print("Offline")
                check = False

            await asyncio.sleep(30)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content in ('아카이로 류', '류', '아카', '대장'):
            await message.channel.send('옴총 귀여워. 알아?')

        if '생일' in message.content and '언제' in message.content:
            await message.channel.send('그것도 몰라? 11월 1일이잖아!! 난 이런 게 서운해🥺')

        if message.content in ('류튜브', '유튜브', '보고싶다'):
            await message.channel.send(offline+'\n https://www.youtube.com/@ryuch.821')

    # async def BangOn_message(self, messege):


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(Token)
