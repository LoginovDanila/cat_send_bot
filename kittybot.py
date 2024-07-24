import os
from dotenv import load_dotenv
from telebot import TeleBot, types
import requests
import logging


load_dotenv()
token = os.getenv('token')
bot = TeleBot(token=token)
URL = 'https://api.thecatapi.com/v1/images/search'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='kittybot.log',
)


def get_new_image():
    try:
        response = requests.get(URL).json()
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url).json()
    random_animal = response[0].get('url')
    return random_animal


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_send_cat = types.KeyboardButton('Пришли котейку!')
    keyboard.add(button_send_cat)
    bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что вы включили меня, {name}!'
        + ' Я умею отправлять котеек!',
        reply_markup=keyboard,
        )


@bot.message_handler(regexp='Пришли котейку!')
def new_cat(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Вот тебе котейка! ' +
                     'P.S. иногда выпадает песик, это нормально!')
    random_cat_url = get_new_image()
    bot.send_photo(chat_id, random_cat_url)


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
