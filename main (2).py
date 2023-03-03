from telebot import TeleBot
from telebot import types
from logic import *
from iso3166 import countries
import apikeys
import sqlite3 as sql

bot = TeleBot(token=apikeys.bot_key)

DEFAULT_CITY = "Moscow"
userBase = {} # [City, CountryCode] for each user
# to replace later with sql when we learn it lmao


def get_user_city(chat_id):
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT city from user_cities WHERE chat_id = (?)", (chat_id,))
    city = cursor.fetchone()
    return city if city else DEFAULT_CITY


def set_user_loc(chat_id, city):
    connection = sql.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("SELECT city FROM user_cities WHERE chat_id = (?)", (chat_id,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO user_cities VALUES(?, ?)", (chat_id, city))
    else:
        cursor.execute("UPDATE user_cities SET city = (?) WHERE chat_id = (?)", (city, chat_id))
    connection.commit()


@bot.message_handler(commands=['set_city'])
def ask_city(message):
    # done = False
    bot.send_message(message.chat.id, "👉Send a message containing your city and country (for example: Moscow, RU): ")
    bot.register_next_step_handler(message, set_city)

def set_city(message):
    if regex_check(message.text) == True: # Moscow, RU
        bot.send_message(message.chat.id, f"✨'{message.text}' set!")
        set_user_loc(int(message.chat.id), str(message.text))
    else:
        by_regex(message)

def by_regex(message): # if the city sent by user is incorrect by regex
    bot.send_message(message.chat.id, f"😔What you've sent us does not follow the example, try again")
    ask_city(message)



@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    weather = get_current_weather(userBase[message.chat.id][0], userBase[message.chat.id][1])
    bot.send_message(message.chat.id, weather)


bot.polling()






