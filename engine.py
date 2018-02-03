from db import DataBaseConnect


def check_id(message):
    connect = DataBaseConnect()
    sample = connect.select_id()
    connect.close_connection()
    return message.reply_to_message.message_id in sample


def add_record(message_id, gist_id):
    connect = DataBaseConnect()
    try:
        connect.new_record(message_id, gist_id)
    finally:
        connect.close_connection()


def get_gist_id(message_id):
    connect = DataBaseConnect()
    try:
        return connect.select_gist_id(message_id)[0][0]
    finally:
        connect.close_connection()
