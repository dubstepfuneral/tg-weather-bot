import telebot
from telebot import TeleBot
from logic import *
from iso3166 import countries
import apikeys
import sqlite3 as sql
import logging

bot = TeleBot(token=apikeys.bot_key)

logging.basicConfig(
    format="%(asctime)s => %(filename)s => %(levelname)s => %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs.txt"
)

main_formatter = logging.Formatter("%(asctime)s => %(filename)s => %(levelname)s => %(message)s")

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(main_formatter)

file_handler = logging.FileHandler(filename="important.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(main_formatter)


root_logger = logging.getLogger("")

root_logger.addHandler(console)
root_logger.addHandler(file_handler)


DEFAULT_CITY = "Moscow, RU"
userBase = {} # [City, CountryCode] for each user
# to replace later with sql when we learn it lmao


def get_user_city(chat_id: int) -> str:
    connection = sql.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT city from user_cities WHERE chat_id = (?)", (chat_id,))
    city = cursor.fetchone()
    return city if city else DEFAULT_CITY


def set_user_loc(chat_id: int, city: str) -> None:
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
def ask_city(message: telebot.types.Message) -> None:
    # done = False
    bot.send_message(message.chat.id, "👉Send a message containing your city and country (for example: Moscow, RU): ")
    bot.register_next_step_handler(message, set_city)

def set_city(message: telebot.types.Message) -> None:
    if regex_check(message.text) == True: # Moscow, RU
        if city_check(message.text) == False:
            by_existence(message)
        bot.send_message(message.chat.id, f"✨'{message.text}' set!")
        set_user_loc(int(message.chat.id), str(message.text))
    else:
        by_regex(message)

def by_regex(message: telebot.types.Message) -> None: # if the city sent by user is incorrect by regex
    bot.send_message(message.chat.id, f"😔What you've sent us does not follow the example, try again")
    ask_city(message)

def by_existence(message: telebot.types.Message) -> None: # if the location sent by user doesn't exist
    bot.send_message(message.chat.id, f"😔Apparently, this location doesn't exist, try again")
    ask_city(message)


@bot.message_handler(regexp="^[A-Za-z]+, [A-Za-z][A-Za-z]$")
def weather_by_message(message: telebot.types.Message) -> None:
    splitString = message.text.split(', ')
    city = splitString[0]
    countryCode = splitString[1]
    weather = get_current_weather(city, countryCode)
    bot.send_message(message.chat.id, weather)



@bot.message_handler(commands=['get_weather'])
def get_weather(message: telebot.types.Message) -> None:
    cityFromDB = get_user_city(message.chat.id)[0] # ex. Moscow, RU
    splitString = cityFromDB.split(', ')
    city = splitString[0]
    countryCode = splitString[1]
    weather = get_current_weather(city, countryCode)
    bot.send_message(message.chat.id, weather)


def city_check(userCity) -> bool: # checking whether or not the city sent by user exists
    splitString = userCity.split(', ')
    city = splitString[0]
    countryCode = splitString[1]
    if get_current_weather(city, countryCode) == "City not found": 
        return False
    else:
        return True


bot.polling()






