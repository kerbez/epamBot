import firebase_admin
from firebase_admin import credentials, db
import telebot
import constants
import datetime
import telegram
from threading import Thread
import time

cred = credentials.Certificate("epam_d1a54_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://epam-d1a54.firebaseio.com'
})
greet_bot = telebot.TeleBot(constants.token)


def notification():
    checked_date = None
    while True:
        if checked_date is not None:
            time.sleep(80000)
        now = datetime.datetime.now()
        print(checked_date, str(now.year) + '-' + str(now.month) + '-' + str(now.day))
        if checked_date == str(now.year) + '-' + str(now.month) + '-' + str(now.day):
            continue
        checked_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        day = now.day
        month = now.month
        year = now.year
        user_ref = db.reference('users')
        order_ref = db.reference('orders')
        book_ref = db.reference('books')
        order_res = order_ref.get()
        ans_dic = {}
        for order in order_res:
            from_owner_id = order_res[order]['from_owner_id']
            user_id = order_res[order]['to_user_id']
            book_id = order_res[order]['book_id']
            start_date = order_res[order]['start_date']
            duration = order_res[order]['duration']
            availability = order_res[order]['availability']
            chat_id = db.reference('teleBot').child('user_to_chat').child(user_id).get()
            now_date = datetime.datetime.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day),
                                                  '%Y-%m-%d')
            end_date = datetime.datetime.strptime(start_date, '%Y-%m-%d') + datetime.timedelta(
                int(duration))
            if availability == 0 and chat_id is not None and end_date <= now_date :
                owner_res = user_ref.child(from_owner_id).get()
                days = ''
                if (now_date - end_date).days == 1:
                    days = 'in ' + str((now_date - end_date).days) + ' day'
                elif (now_date - end_date).days == 0:
                    days = 'today'
                elif (now_date - end_date).days > 1:
                    days = str((now_date - end_date).days) + ' days ago'
                elif (now_date - end_date).days == -1:
                    days = 'tomorrow'
                else:
                    days = 'in ' + str((now_date - end_date).days) + ' days'
                if chat_id not in ans_dic:
                    ans_dic[chat_id] = 'You need to return'
                ans_dic[chat_id] += '\n \'*' + book_ref.child(book_id).child('title').get() + '*\' book to *' + \
                                    owner_res['first_name'] + '* ' + days
        for ans in ans_dic:
            greet_bot.send_message(ans, ans_dic[ans], parse_mode=telegram.ParseMode.MARKDOWN)
        # order_ref = db.reference('orders')
        # order_res = order_ref.get()
        # book_ref = db.reference('books')
        # user_ref = db.reference('users')
        # for key in order_res:
        #     print(order_res[key]['start_date'])
        #     now_date = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d')
        #     end_date = datetime.datetime.strptime(order_res[key]['start_date'], '%Y-%m-%d') + datetime.timedelta(
        #         int(order_res[key]['duration']) - 1)
        #     print(now_date, end_date)
        #     if end_date <= now_date and order_res[key]['availability'] == 0:
        #         print(end_date, now_date)
        #         difference = now_date - end_date
        #         print(difference)
        #         to_user_id = order_res[key]['to_user_id']
        #         from_owner_id = order_res[key]['from_owner_id']
        #         book_id = order_res[key]['book_id']
        #         user_res = user_ref.child(to_user_id).get()
        #         chat_id = user_res['chat_id']
        #         print(from_owner_id, to_user_id, book_id, chat_id)
        #         if chat_id == '-':
        #             continue
        #         owner_res = user_ref.child(from_owner_id).get()
        #         book_res = book_ref.child(book_id).get()
        #         print(user_res)
        #         if difference.days == 0:
        #             message = 'Dear ' + user_res['first_name'] + \
        #                       ', you have a day to read and return the \'*' + book_res['title'] + '*\' book to *' + \
        #                       owner_res['first_name']+'*'
        #         elif difference.days == 1:
        #             message = 'Dear ' + user_res['first_name'] + \
        #                       ', today you need to return the \'*' + book_res['title'] + '*\' book to *' + \
        #                       owner_res['first_name']+'*'
        #         elif difference.days == 2:
        #             message = 'Dear ' + user_res['first_name'] + ', ' + str(difference.days-1) + \
        #                       ' day ago you should have returned the \'*' + book_res['title'] + '*\' book to *' + \
        #                       owner_res['first_name']+'*'
        #         else:
        #             message = 'Dear ' + user_res['first_name'] + ', ' + str(difference.days-1) + \
        #                       ' days ago you should have returned the \'*' + book_res['title'] + '*\' book to *' + \
        #                       owner_res['first_name']+'*'
        #         greet_bot.send_message(int(chat_id), message, parse_mode=telegram.ParseMode.MARKDOWN)
        #     else:
        #         continue


t = Thread(target=notification)
t.start()


@greet_bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    telebot_res = db.reference('teleBot').child('chat_to_user').child(str(chat_id)).get()
    print(telebot_res)
    if telebot_res is not None:
        greet_bot.send_message(message.chat.id, 'If you want to reset your email, just give me your new email')
    else:
        greet_bot.send_message(message.chat.id, "Hi " + message.from_user.first_name + ', I\'m a bot Epam')
        greet_bot.send_message(message.chat.id, 'Can you give your email?')


@greet_bot.message_handler(commands=['help'])
def handle_help(message):
    chat_id = message.chat.id
    telebot_res = db.reference('teleBot').child('chat_to_user').child(str(chat_id)).get()
    print(telebot_res)
    answer = ''
    if telebot_res is None:
        answer = '\n I see you didn\'t specify an email. Please give me your email'
    add_mes = '/start \t start bot dialog \n/help \t list of all commands \n/list \t list of books you lent'
    greet_bot.send_message(chat_id, "I'm Epam bot. I can help you, if you are registered in the Epam\'s *Library* application" + answer + '\n' + add_mes, parse_mode=telegram.ParseMode.MARKDOWN)


@greet_bot.message_handler(commands=['list'])
def handle_list(message):
    chat_id = message.chat.id
    telebot_res = db.reference('teleBot').child('chat_to_user').child(str(chat_id)).get()
    print(telebot_res)
    if telebot_res is None:
        greet_bot.send_message(message.chat.id, 'I see you didn\'t specify an email. Please give me your email')
    else:
        now = datetime.datetime.now()
        answer = 'You need to return'
        user_id = telebot_res
        user_res = db.reference('users').child(user_id).get()
        order_ref = db.reference('orders')
        book_ref = db.reference('books')
        order_res = order_ref.get()
        for order in order_res:
            if order_res[order]['to_user_id'] == user_id and order_res[order]['availability'] == 0:
                now_date = datetime.datetime.strptime(str(now.year) + '-' + str(now.month) + '-' + str(now.day), '%Y-%m-%d')
                end_date = datetime.datetime.strptime(order_res[order]['start_date'], '%Y-%m-%d') + datetime.timedelta(
                    int(order_res[order]['duration']))
                from_owner_id = order_res[order]['from_owner_id']
                owner_res = db.reference('users').child(from_owner_id).get()
                book_id = order_res[order]['book_id']
                days = ''
                if (now_date - end_date).days == 1:
                    days = 'in ' + str((now_date - end_date).days) + ' day'
                elif (now_date - end_date).days == 0:
                    days = 'today'
                elif (now_date - end_date).days > 1:
                    days = str((now_date - end_date).days) + ' days ago'
                elif (now_date - end_date).days == -1:
                    days = 'tomorrow'
                else:
                    days = 'in ' + str((now_date - end_date).days) + ' days'
                answer += '\n \'*'+book_ref.child(book_id).child('title').get()+'*\' book to *' + owner_res['first_name'] + '* ' + days
        greet_bot.send_message(message.chat.id, answer, parse_mode=telegram.ParseMode.MARKDOWN)


@greet_bot.message_handler()
def handle_message(message):
    is_ok = 0
    if '@' in message.text:
        for mes in message.text.split():
            if '@' in mes:
                print('hmm')
                chat_id = message.chat.id
                user_ref = db.reference('users').get()
                for key in user_ref:
                    print(key)
                    if mes.lower() == user_ref[key]['email']:
                        is_ok = 1
                        print(user_ref[key]['first_name'])
                        user_res = db.reference('users').child(key)
                        user_res.update({
                            'chat_id': chat_id
                        })
                        telebot_res = db.reference('teleBot')
                        telebot_res.child('user_to_chat').update({
                            key: chat_id
                        })
                        telebot_res.child('chat_to_user').update({
                            chat_id: key
                        })
                        greet_bot.send_message(message.chat.id, 'Cool! We will warn you about return of the book')
                        greet_bot.send_message(message.chat.id,
                                               'If you want to reset your email, just give me your new email')
        if is_ok == 0:
            greet_bot.send_message(message.chat.id, 'I think you wrote wrong email, try again')


now = datetime.datetime.now()


greet_bot.polling(none_stop=True, interval=0)






