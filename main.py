

import time
from chzzkApi.chzzkbotapi import ChzzkBotApi

"""
config파일의 형식 예시
import json
with open('config.json','w',encoding='utf-8') as f:
    f.write(json.dumps(
        {
            "app_data": {
                "client_id": "your_client_id",
                "client_secret": "your_client_secret",
                "redirect_uri": "http://example.com",
                "uri_state": "teststate"
            },
            "authorization_data": {
                "authorization_token": "yout_auth_token",
                "access_token": "your_acc_token",
                "refresh_token": "your_ref_token",
                "expires_in": your_expires_in + time.time() # 만료시각
            }
        }
    ))
"""

chzzkbot = ChzzkBotApi(config='config.json')
chzzkbot.authorization.get_authorization_token()

if time.time() > chzzkbot.authorization.expires_in:
    chzzkbot.authorization.get_access_token(get_type='refresh')
    print('access_token refreshed')

@chzzkbot.event('CHAT')
async def chat_event(data):
    print(data)
    if data.message[:4] == '!공지 ': # '!공지 테스트'라고 메세지 보내면 '테스트' 부분이 공지로 등록됨
        chzzkbot.set_notice(data.message[4:])
    elif data.message == '안녕':
        chzzkbot.send_message('안녕!')


@chzzkbot.event('DONATION')
async def chat_event(data):
    print(data)


chzzkbot.connect_session()