from .chzzkbot_api_auth import ChzzkbotApiAuthorization
from .session_data_types import *
import requests
import socketio
import asyncio
import json

class ChzzkBotApi:
    def __init__(self, config: str='config.json'):
        self.authorization = ChzzkbotApiAuthorization(config=config)
        self.base_url = 'https://openapi.chzzk.naver.com'

        self.streamer_nickname = None
        self.streamer_uid = None
        self.client_session_url = None
        self.user_session_url = None

        self.event_handlers = {}

        self.sio = None

    def get_headers(self, show_authorization=True, show_content_type=True, show_client_id=True, show_client_secret=True):
        data = {}
        if show_authorization:
            data["Authorization"] = f"Bearer {self.authorization.access_token}"
        if show_content_type:
            data["Content-Type"] = "application/json"
        if show_client_id:
            data["Client-Id"] = self.authorization.client_id
        if show_client_secret:
            data["Client-Secret"] = self.authorization.client_secret
        return data

    def get_channel_info(self):
        """
        채널 정보 조회
        """
        if not self.authorization.access_token:
            raise AttributeError('access_token is None. Login first!')

        url = self.base_url + "/open/v1/users/me"
        headers = {
            "Authorization": f"Bearer {self.authorization.access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            self.streamer_uid = result['content']['channelId']
            self.streamer_nickname = result['content']['nickname']
            return result
        else:
            print("내 유저 정보 조회 실패:", response.status_code, response.text)
            raise Exception("내 유저 정보 조회 실패")

    def send_message(self,message: str):
        if not self.authorization.access_token:
            raise AttributeError('acc_token is None. Login first!')
        if len(message) > 100:
            raise Exception("메세지는 100자를 넘길 수 없습니다.")
        if len(message) == 0:
            raise Exception("메세지는 빈 문자열일 수 없습니다.")

        url = self.base_url + "/open/v1/chats/send"

        headers = self.get_headers()
        data = {
            "message":message
        }
        response = requests.post(url, json=data, headers=headers)
        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            raise Exception(f"메세지 전송 실패: {response.text}")

    def set_notice(self,message: str):
        if not self.authorization.access_token:
            raise AttributeError('access_token is None. Login first!')
        if len(message) > 100:
            raise Exception("공지 메세지는 100자를 넘길 수 없습니다.")

        url = self.base_url + "/open/v1/chats/notice"

        headers = self.get_headers()
        data = {
            "message":message
        }
        response = requests.post(url, json=data, headers=headers)
        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            raise Exception(f"공지 등록 실패: {response.text}")

    def get_client_session_url(self):
        if not self.authorization.access_token:
            raise AttributeError('access_token is None. Login first!')

        url = self.base_url + "/open/v1/sessions/auth/client"

        headers = self.get_headers(show_authorization=False)
        response = requests.get(url, headers=headers)

        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            print(result)
            return result['content']['url']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            #raise Exception(f"오류: {response.text}")

    def sub_chat(self, key):
        url = self.base_url + "/open/v1/sessions/events/subscribe/chat?sessionKey=" + key
        print(url)

        headers = self.get_headers()

        response = requests.post(url, headers=headers)
        return response

    def get_client_session_url(self):
        """
        클라이언트 세션 url 획득 / 안씀..
        :return:
        """
        if not self.authorization.access_token:
            raise AttributeError('access_token is None. Login first!')

        url = self.base_url + "/open/v1/sessions/auth/client"

        headers = self.get_headers(show_authorization=False)
        response = requests.get(url, headers=headers)

        # 응답 처리
        if response.status_code == 200:
            result = response.json()
            return result['content']['url']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            # raise Exception(f"오류: {response.text}")

    def get_user_session_url(self):
        """
        유저 세션 url 획득
        :return:
        """
        if not self.authorization.access_token:
            raise AttributeError('access_token is None. Login first!')

        url = self.base_url + "/open/v1/sessions/auth"

        headers = self.get_headers()
        response = requests.get(url, headers=headers)

        # 응답 처리
        if response.status_code == 200:
            result = response.json()['content']['url']
            return result
        else:
            print(f"Error: {response.status_code}, {response.text}")
            # raise Exception(f"오류: {response.text}")

    def get_client_session_list(self, size=50, page=0):
        """
        클라이언트 세션 목록 획득

        :param size:
        :param page:
        :return:
        """
        if not self.authorization.access_token:
            raise AttributeError('access_token is None. Login first!')
        url = self.base_url + "/open/v1/sessions/client"

        headers = self.get_headers(show_authorization=False)
        data = {
            "size": size,  # 한번에 조회할 세션 수: 1~50
            "page": page,  # 조회할 페이지: 0~
        }

        response = requests.get(url, json=data, headers=headers)
        return response.json()

    def sub_chat(self, key):
        """
        세션 이벤트(채팅) 구독
        :param key:
        :return:
        """
        url = self.base_url + "/open/v1/sessions/events/subscribe/chat?sessionKey=" + key
        headers = self.get_headers()
        response = requests.post(url, headers=headers)
        return response

    def sub_donation(self, key):
        """
        세션 이벤트(도네) 구독
        :param key:
        :return:
        """
        url = self.base_url + "/open/v1/sessions/events/subscribe/donation?sessionKey=" + key
        headers = self.get_headers()
        response = requests.post(url, headers=headers)
        return response

    def event(self, event_name):
        """이벤트 핸들러를 등록하는 데코레이터"""

        def decorator(func):
            self.event_handlers[event_name.upper()] = func
            return func

        return decorator

    def process_data(self, event, data):
        """핸들러에 반환할 데이터로 변환하는 함수"""
        if event == "CHAT":
            return Chat(data)
        elif event == "DONATION":
            return Donation(data)
        return json.loads(data)

    async def disconnect_session(self):
        await self.sio.disconnect()

    async def run_session(self):
        """세션 연결 및 태스크 작동"""

        # 세션 연결
        session_url = self.get_client_session_url()

        self.sio = socketio.AsyncClient()

        @self.sio.event
        async def connect():
            print('connected')

        @self.sio.event
        async def disconnect():
            print('disconnected')
            self.connect_session()

        @self.sio.on('SYSTEM')
        async def system_msg(data):
            data = json.loads(data)
            print(data)
            if data['type'] == 'connected':
                session_key = data['data']['sessionKey']
                self.sub_chat(session_key)
                self.sub_donation(session_key)

        for event, handler in self.event_handlers.items():
            @self.sio.on(event)
            async def event_handler(data, handler=handler, event=event):
                await handler(self.process_data(event, data))

        """
        @self.sio.on('CHAT')
        async def read_chat(data):
            data = json.loads(data)


        @self.sio.on('DONATION')
        async def read_donation(data):
            data = json.loads(data)
        """

        await self.sio.connect(session_url, transports=['websocket'])

        # 대기
        await self.sio.wait()

    def connect_session(self):
        """유저가 세션 연결/실행시키기"""
        asyncio.run(self.run_session())
