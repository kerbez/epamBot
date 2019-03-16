import firebase_admin
from firebase_admin import credentials, db
import telebot
import constants
import datetime
import requests


cred = credentials.Certificate("epam_d1a54_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://epam-d1a54.firebaseio.com'
})

greet_bot = telebot.TeleBot(constants.token)


class Notification:
    def main(self):
        checked_date = None
        while True:
            now = datetime.datetime.now()
            print(checked_date, str(now.year) + '-' + str(now.month) + '-' + str(now.day))
            if checked_date == str(now.year) + '-' + str(now.month) + '-' + str(now.day):
                continue
            checked_date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
            day = now.day
            month = now.month
            year = now.year
            order_ref = db.reference('orders')
            order_res = order_ref.get()
            book_ref = db.reference('books')
            user_ref = db.reference('users')
            for key in order_res:
                print(order_res[key]['start_date'])
                now_date = datetime.datetime.strptime(str(year) + '-' + str(month) + '-' + str(day), '%Y-%m-%d')
                end_date = datetime.datetime.strptime(order_res[key]['start_date'], '%Y-%m-%d') + datetime.timedelta(
                    int(order_res[key]['duration']) - 1)
                print(now_date, end_date)
                if end_date <= now_date and order_res[key]['availability'] == 0:
                    print(end_date, now_date)
                    difference = now_date - end_date
                    print(difference)
                    to_user_id = order_res[key]['to_user_id']
                    from_owner_id = order_res[key]['from_owner_id']
                    book_id = order_res[key]['book_id']
                    user_res = user_ref.child(to_user_id).get()
                    chat_id = user_res['chat_id']
                    print(from_owner_id, to_user_id, book_id, chat_id)
                    if chat_id == '-':
                        continue
                    owner_res = user_ref.child(from_owner_id).get()
                    book_res = book_ref.child(book_id).get()
                    print(user_res)
                    if difference.days == 0:
                        message = 'Dear ' + user_res['last_name'] + ' ' + user_res['first_name'] + \
                                  ', you have a day to read and return the \'' + book_res['title'] + '\' book to ' + \
                                  owner_res['last_name'] + ' ' + owner_res['first_name']
                    elif difference.days == 1:
                        message = 'Dear ' + user_res['last_name'] + ' ' + user_res['first_name'] + \
                                  ', today you need to return the \'' + book_res['title'] + '\' book to ' + \
                                  owner_res['last_name'] + ' ' + owner_res['first_name']
                    else:
                        message = 'Dear ' + user_res['last_name'] + ' ' + user_res['first_name'] + ', ' + str(
                            difference.days) + \
                                  ' days ago you should have returned the \'' + book_res['title'] + '\' book to ' + \
                                  owner_res['last_name'] + ' ' + owner_res['first_name']
                    greet_bot.send_message(int(chat_id), message)
                else:
                    continue

    if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            exit()
