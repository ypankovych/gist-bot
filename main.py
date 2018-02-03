import os

import engine
import requests
import telebot

link = 'https://t.me/{}/{}'
bot = telebot.TeleBot(os.environ.get('token'))
make_gist = 'https://api.github.com/gists'


@bot.message_handler(commands=['paste'])
def create_gist(message):
    if message.reply_to_message and message.reply_to_message.text:
        if not engine.check_id(message):
            return send_gist(message)
        bot.reply_to(message,
                     text=link.format(message.chat.username,
                                      engine.get_gist_id(message.reply_to_message.message_id)))
    else:
        bot.delete_message(message.chat.id, message.message_id)


@bot.message_handler(commands=['start'], func=lambda message: message.chat.type == 'private')
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Add to group',
                                                  url='t.me/g1st_bot?startgroup=on'))
    bot.send_message(chat_id=message.chat.id,
                     text='Add me to your group and promote to admin.\nTo call me just type /paste',
                     reply_markup=markup)


def send_gist(message):
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
    gist_id = bot.reply_to(message.reply_to_message, text=gist['html_url'])
    engine.add_record(message.reply_to_message.message_id, gist_id.message_id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
