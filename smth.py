# class BotHandler:
#
#     def __init__(self, token):
#         self.token = token
#         self.api_url = "https://api.telegram.org/bot{}/".format(token)
#
#     def get_updates(self, offset=None, timeout=30):
#         method = 'getUpdates'
#         params = {'timeout': timeout, 'offset': offset}
#         resp = requests.get(self.api_url + method, params)
#         result_json = resp.json()['result']
#         return result_json
#
#     def send_message(self, chat_id, text):
#         params = {'chat_id': chat_id, 'text': text}
#         method = 'sendMessage'
#         resp = requests.post(self.api_url + method, params)
#         return resp
#
#     def get_last_update(self):
#         get_result = self.get_updates()
#
#         if len(get_result) > 0:
#             last_update = get_result[-1]
#         else:
#             last_update = get_result[len(get_result)]
# bot = telebot.TeleBot(constants.token)
# print(constants.token)
# #bot.send_message(783659796, "test");
#
# upd = bot.get_updates();
# #print(upd)
# """
# last_upd = upd[-1]
# message_from_user = last_upd.message
# print(message_from_user)
# """
#
# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     if message.text == "Hi" or message.text == "hi":
#         bot.send_message(message.chat.id, "Hi "+message.from_user.first_name)
#         print(message)
#         # requests.post('https://accounts.google.com/o/oauth2/revoke',
#         #               params={'token': credentials.token},
#         #
#         #               headers={'content-type': 'application/x-www-form-urlencoded'})
#
#     else:
#         print("in else")
#         bot.send_message(message.chat.id, "Hii " + message.from_user.first_name)
#         print(message)
#
#
#         return last_update

# greet_bot.send_message(783659796, 'Dear {}, its time to return book'.format(difference.days))
# new_offset = None
# today = now.day
# hour = now.hour
# while True:

# greet_bot.get_updates(new_offset)
#
# last_update = greet_bot.get_last_update()
# print(last_update)
# last_update_id = last_update['update_id']
# last_chat_text = last_update['message']['text']
# last_chat_id = last_update['message']['chat']['id']
# last_chat_name = last_update['message']['chat']['first_name']
#
# if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
#     greet_bot.send_message(last_chat_id, 'dobroe utro, {}'.format(last_chat_name))
#     today += 1
#
# elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
#     greet_bot.send_message(last_chat_id, 'dobryi den, {}'.format(last_chat_name))
#     today += 1
#
# elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
#     greet_bot.send_message(last_chat_id, 'dobryi vecher, {}'.format(last_chat_name))
#     today += 1
#
# new_offset = last_update_id + 1
