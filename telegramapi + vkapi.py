import telebot
import vk_api
import configparser
from config import API_KEY


bot = telebot.TeleBot(API_KEY)

config = configparser.ConfigParser()
config.read("config.ini")

session = vk_api.VkApi(token=config['VK']['token'])
vk = session.get_api()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Получить список друзей')
    bot.send_message(message.chat.id, '👋', reply_markup=markup)
    bot.send_message(message.chat.id, '732636338', reply_markup=markup)


@bot.message_handler(regexp='Получить список друзей')
def echo_message(message):
    def get_friends(user_id):
        friends = session.method('friends.get', {'user_id': user_id})
        # online = session.method('friends.getOnline', {'user_id': user_id})
        for friend_id, friend in enumerate(friends['items']):
            user = session.method('users.get', {'user_ids': friend})
            bot.send_message(message.chat.id,
                             text=f'{friend_id + 1}: {user[0]["id"]}, {user[0]["first_name"]}, {user[0]["last_name"]}')

    get_friends('732636338')


bot.infinity_polling()
