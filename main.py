import os

import requests
import telebot

bot = telebot.TeleBot(os.environ.get('token'))
make_gist = 'https://api.github.com/gists'


@bot.message_handler(commands=['paste'])
def create_gist(message):
    if message.reply_to_message and message.reply_to_message.text:
        payload = {
            "description": f"From {message.reply_to_message.from_user.first_name}",
            "public": 'true',
            "files": {
                "file1.py": {
                    "content": message.reply_to_message.text
                }
            }
        }
        gist = requests.post(make_gist, json=payload, timeout=1000).json()
        bot.reply_to(message.reply_to_message, text=gist['html_url'])


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Add to group',
                                                  url='t.me/g1st_bot?startgroup=on'))
    bot.send_message(chat_id=message.chat.id,
                     text='Add me to your group and promote to admin.\nTo call me just type /paste',
                     reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
