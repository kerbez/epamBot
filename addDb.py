import firebase_admin
from firebase_admin import credentials, db
import datetime

cred = credentials.Certificate("epam_d1a54_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://epam-d1a54.firebaseio.com'
})

time = datetime.datetime.now();


ref = db.reference()
orders_ref = ref.child('orders')
users_ref = ref.child('users')
books_ref = ref.child('books')
teleBot_ref = ref.child('teleBot')
teleBot_ref.set({
    'chat_to_user': {
        '7836597': 'asss',
    },
    'user_to_chat': {
        'asss': '783659795',
    },
})
# orders_ref.set({
#     'a': {
#         'from_owner_id': 'asssa',
#         'to_user_id': 'adnfs',
#         'book_id': 'bsdf',
#         'start_date': '2019-03-10',
#         'duration': '3',
#         'availability':'False',
#     },
#     'b': {
#         'from_owner_id': 'adnfs',
#         'to_user_id': 'asssa',
#         'book_id': 'ssdf',
#         'start_date': '2019-03-13',
#         'duration': '3',
#         'availability':'False',
#     },
# })
# users_ref.set({
#     'asssa':{
#         'first_name': 'Kerbez',
#         'last_name' : 'Orazgaliyeva',
#         'email' : 'kerbez2898@gmail.com',
#         'book_ids' : 'bsdf, bsde, bsda',
#     },
#     'adnfs':{
#         'first_name': 'Sanzhar',
#         'last_name' : 'Alim',
#         'email' : 'alim@gmail.com',
#         'book_ids' : 'ssdf, ssde, ssda',
#     }
# })
# books_ref.set({
#     'bsdf':{
#         'title':'Harry Potter and stone',
#         'author':'',
#         'description':'',
#         'image_path':'',
#         'rate_ids':'',
#         'availability':'False',
#         'order_ids':'a'
#     },
#     'bsde':{
#         'title': '',
#         'author': '',
#         'description': '',
#         'image_path': '',
#         'rate_ids': '',
#         'availability': 'True',
#         'order_ids': ''
#     },
#     'bsda':{
#         'title': '',
#         'author': '',
#         'description': '',
#         'image_path': '',
#         'rate_ids': '',
#         'availability': 'True',
#         'order_ids': ''
#     },
#     'ssdf':{
#         'title': 'kruassany',
#         'author': 'Yashkino',
#         'description': '',
#         'image_path': '',
#         'rate_ids': '',
#         'availability': 'False',
#         'order_ids': 'b'
#     },
#     'ssde':{
#         'title': '',
#         'author': '',
#         'description': '',
#         'image_path': '',
#         'rate_ids': '',
#         'availability': 'True',
#         'order_ids': ''
#     },
#     'ssda':{
#         'title': '',
#         'author': '',
#         'description': '',
#         'image_path': '',
#         'rate_ids': '',
#         'availability': 'True',
#         'order_ids': ''
#     },
# })