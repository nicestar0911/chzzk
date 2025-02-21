
chzzk 공식 API 사용을 돕는 패키지입니다.

사용법 예제

```python
import time
from chzzkApi.chzzkbotapi import ChzzkBotApi

"""
초기 config파일의 형식 예시. 모듈에서 인증 정보 얻으면 여기에 저장됨.
app_data 부분은 필수로 채워두고, authorization 부분은 로그인 진행하면 프로그램이 채워줌.

import json
with open('config.json','w',encoding='utf-8') as f:
    f.write(json.dumps(
        {
            "app_data": {
                "client_id": "your_client_id", # 앱 client id
                "client_secret": "your_client_secret", # 앱 client secret
                "redirect_uri": "http://example.com/api/login", # 앱에 등록한 redirect uri
                "uri_state": "teststate" # authorization token 얻을때 쓸 state
            },
            "authorization_data": {
                "authorization_token": "yout_auth_token", # authorization token값
                "access_token": "your_acc_token", # access token값
                "refresh_token": "your_ref_token", # refresh token값
                "expires_in": your_expires_in # 만료시각: int((응답받은 expires_in) + time.time())값
            }
        }
    ))
"""

chzzkbot = ChzzkBotApi(config='config.json')

# 로그인 진행(authorization 코드 입력 단계부터
# 이전에 로그인해 config.json에 데이터가 저장되어 있다면 해당 코드는 주석처리하고 단순 불러오기 or 재발급만 해도 됨.)
chzzkbot.authorization.get_authorization_token()

# 토큰 유효기간이 지났을 경우 재발급 
if time.time() > chzzkbot.authorization.expires_in:
    chzzkbot.authorization.get_access_token(get_type='refresh')
    print('access_token refreshed')

# 채팅 이벤트 수신 시 작동
@chzzkbot.event('CHAT')
async def chat_event(data):
    print(data)
    if data.message[:3] == '!공지': # '!공지 테스트'라고 메세지 보내면 '테스트' 부분이 공지로 등록됨
        chzzkbot.set_notice(data.message[3:])
    elif data.message == '안녕':
        chzzkbot.send_message('안녕!')

# 도네이션 이벤트 수신 시 작동
@chzzkbot.event('DONATION')
async def chat_event(data):
    print(data)

# 채팅 연결
chzzkbot.connect_session()
```

---

계정 인증(authorization_token 입력):
```python
# authorization_token 입력하면 access_token 획득까지 자동으로 진행됨.

# input()로 입력: 실행시 링크가 나오며, 링크로 이동 후 연결할 스트리머 계정으로 로그인한 후 code를 입력해주세요
chzzkbot.authorization.get_authorization_token()

# 또는 문자열로 직접 입력하기
chzzkbot.authorization.set_authorization_token('your_authorization_token')
```

계정 인증(access_token 획득)
```python
# access_token, refresh_token, expires_in 획득 - 미리 authorization_token이 입력되어있어야함.
chzzkbot.authorization.get_access_token('get')

# 또는 직접 입력하기
chzzkbot.authorization.set_access_token('your_access_token')
chzzkbot.authorization.set_refresh_token('your_refresh_token')
```

계정 인증(access_token 재발급)
```python
# 새 access_token, refresh_token, expires_in 획득 - 미리 refresh_token이 입력되어 있어야 함.
chzzkbot.authorization.get_access_token('refresh')
```

---

채팅 보내기:
```python
chzzkbot.send_message('보낼 메세지')
```
공지 쓰기:
```python
chzzkbot.set_notice('공지 메세지')
```
채널 정보 획득:
```python
chzzkbot.get_channel_info()
```

---

채팅 연결:
```python

# 채팅 이벤트 수신 시 작동
@chzzkbot.event('CHAT')
async def chat_event(data):
    print(data)
    if data.message[:3] == '!공지':
        chzzkbot.set_notice(data.message[3:])
    elif data.message == '안녕':
        chzzkbot.send_message('안녕!')

# 도네이션 이벤트 수신 시 작동
@chzzkbot.event('DONATION')
async def chat_event(data):
    print(data)

# 채팅 연결
chzzkbot.connect_session()
```

참고 - 채팅/도네이션 이벤트 수신시 받는 데이터 형식:
```
Chat:
    data: (dict) 수신 원본 데이터
    channel_uid: (str) 채널 uid
    uid: (str) 메세지 보낸사람 uid
    nickname: (str) 메세지 보낸사람 닉네임
    message: (str) 메세지 내용
    message_time: (int) 메세지 보낸 시각
    emojis: (dict) 이모티콘 참고 정보(이미지 url 등)
    badges: (list) 보유 뱃지 정보

Donation:
    data: (dict) 수신 원본 데이터
    type: (str) 도네 타입: 'VIDEO' / 'CHAT'
    channel_uid: (str) 채널 uid
    uid: (str) 보낸사람 uid / 익명일경우 'anonymous'
    nickname: (str) 보낸사람 닉 / 익명일경우 ''
    pay_amount: (int) 도네 금액
    message: (str) 도네 메세지 / 영상도네일경우 영상제목
```
