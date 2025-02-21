import json


class Chat:
    def __init__(self, data):
        self.data = json.loads(data)
        self.channel_uid = self.data['channelId']
        self.uid = self.data['senderChannelId']
        self.nickname = self.data['profile']['nickname']
        self.message = self.data['content']
        self.message_time = self.data['messageTime']
        self.emojis = self.data['emojis']
        self.badges = self.data['profile']['badges']
    def __str__(self):
        res = f'{vars(self)}'[1:-1]
        return f'Chat({res})'


class Donation:
    def __init__(self, data):
        self.data = json.loads(data)
        self.type = self.data['donationType']
        self.uid = self.data['donatorChannelId']
        self.nickname = self.data['donatorNickname']
        self.pay_amount = self.data['payAmount']
        self.message = self.data['donationText']
    def __str__(self):
        res = f'{vars(self)}'[1:-1]
        return f'Chat({res})'
