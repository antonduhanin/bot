import datetime

import requests
from time import sleep

url = "https://api.telegram.org/bot659162348:AAHI4kbFbxslyLZD5GsjdBDl-_3aqQ0Wbt4/"


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
        self.last_update_id = 0

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        if ('message' in last_update and self.last_update_id == 0):
            self.last_update_id = last_update['message']['message_id']
            return ''
        elif ('message' in last_update and self.last_update_id != last_update['message']['message_id']):
            self.last_update_id = last_update['message']['message_id']
            return last_update
        else:
            return ''


greet_bot = BotHandler('659162348:AAHI4kbFbxslyLZD5GsjdBDl-_3aqQ0Wbt4')


def main():
    now = datetime.datetime.now()

    hour = now.hour
    count = 2
    while True:
        greet_bot.get_updates()

        last_update = greet_bot.get_last_update()
        now = datetime.datetime.now()

        if last_update != '':
            last_chat_text = last_update['message']['text']
            last_chat_id = last_update['message']['chat']['id']
            name = last_update['message']['from']['first_name']

            if last_chat_text == '/petuh' and hour != now.hour:
                count += 1
                s = str("Oleg petuh of the day : " + str(count) + " time")
                greet_bot.send_message(last_chat_id, s)
                hour = now.hour
            elif last_chat_text == '/petuh':
                greet_bot.send_message(last_chat_id, 'try later please')
                greet_bot.send_message(last_chat_id, 'What a moron!!!')
            elif name == 'Oleg':
                greet_bot.send_message(last_chat_id, 'Петухам' + str(count) + '-разовым слово не давали')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
