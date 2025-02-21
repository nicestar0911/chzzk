import requests
import time
import json

class ChzzkbotApiAuthorization:
    def __init__(self, config=None):
        self.config = config

        # base info
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.state = 'default_state'

        self.authorization_token = None
        self.access_token = None
        self.refresh_token = None
        self.expires_in = None

        if self.config is not None:
            with open(self.config, 'r', encoding='utf-8') as file:
                config_data = json.load(file)
            self.client_id = config_data['app_data']['client_id']
            self.client_secret = config_data['app_data']['client_secret']
            self.redirect_uri = config_data['app_data']['redirect_uri']
            self.state = config_data['app_data']['uri_state']

            if config_data['authorization_data']['authorization_token']:
                self.authorization_token = config_data['authorization_data']['authorization_token']
            if config_data['authorization_data']['refresh_token']:
                self.authorization_token = config_data['authorization_data']['refresh_token']
            if config_data['authorization_data']['access_token']:
                self.access_token = config_data['authorization_data']['access_token']
            if config_data['authorization_data']['expires_in']:
                self.expires_in = config_data['authorization_data']['expires_in']

        # auth info

        self.request_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

    def __str__(self):
        return (f'Authorization('
                f'client_id:"{self.client_id}", '
                f'client_secret:"{self.client_secret}", '
                f'redirect_uri:"{self.redirect_uri}", '
                f'state:"{self.state}", '
                f'authorization_token: "{self.authorization_token}", '
                f'access_token: "{self.access_token}", '
                f'refresh_token: "{self.refresh_token}", '
                f'expires_in: {self.expires_in}'
                f')')

    def save_config_file(self):
        data = {
            "app_data": {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "redirect_uri": self.redirect_uri,
                "uri_state": self.state
            },
            "authorization_data": {
                "authorization_token": self.authorization_token,
                "access_token": self.access_token,
                "refresh_token": self.refresh_token,
                "expires_in": self.expires_in
            }
        }
        with open(self.config, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4) # type: ignore

    def get_authorization_token(self):
        url = (
            f'https://chzzk.naver.com/account-interlock'
            f'?clientId={self.client_id}'
            f'&redirectUri={self.redirect_uri}'
            f'&state={self.state}'
        )

        print(url)
        self.authorization_token = input('code? \n -> ')
        self.save_config_file()

        self.get_access_token(get_type='get')

    def set_authorization_token(self, authorization_token):
        self.authorization_token = authorization_token
        self.save_config_file()
        return self.authorization_token

    def get_access_token(self, get_type: str='get'):
        """
        :param get_type:  Specifies the method to retrieve the access token.
            - 'get': Issues a new access token.
            - 'refresh': Reissues an access token using a refresh method.
        :return:
        """
        if self.client_id is None:
            print('client_id is None')
            return None
        if self.client_secret is None:
            print('client_secret is None')
            return None

        url = 'https://chzzk.naver.com/auth/v1/token'

        if get_type == 'get':
            if self.authorization_token is None:
                print('authorization_token is None')
                return None
            send_data = {
                'grantType': 'authorization_code',
                'clientId': self.client_id,
                'clientSecret': self.client_secret,
                'code': self.authorization_token,
                'state': self.state
            }
        elif get_type == 'refresh':
            if self.refresh_token is None:
                print('refresh_token is None')
                return None
            send_data = {
                'grantType': 'refresh_token',
                'refreshToken': self.refresh_token,
                'clientId': self.client_id,
                'clientSecret': self.client_secret
            }
        else:
            print('invalid get_type')
            return None

        response = requests.post(url, json=send_data)
        try:
            response_json = response.json()
        except ValueError:
            print("Failed to parse response as JSON.")
            return None

        if response.status_code == 200:
            self.refresh_token = response_json['content']['refreshToken']
            self.access_token = response_json['content']['accessToken']
            self.expires_in = response_json['content']['expiresIn'] + time.time()
            self.save_config_file()
            return self.access_token
        else:
            print(f'[Error {response.status_code}]: {response_json}')
            return None

    def set_access_token(self, access_token):
        self.access_token = access_token
        self.save_config_file()
        return self.access_token

    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token
        self.save_config_file()
        return self.refresh_token

if __name__ == '__main__':
    auth = ChzzkbotApiAuthorization(config='config.json')
    auth.get_authorization_token()
    print(str(auth))