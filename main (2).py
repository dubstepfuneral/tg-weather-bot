from telebot import TeleBot
from telebot import types
from logic import *
from iso3166 import countries
import apikeys

bot = TeleBot(token=apikeys.bot_key)

userBase = {} # [City, CountryCode] for each user
# to replace later with sql when we learn it lmao



@bot.message_handler(commands=['set_city'])
def ask_city(message):
    # done = False
    bot.send_message(message.chat.id, "👉Send a message containing your city and country (for example: Moscow, RU): ")
    if regex_check(message.text) == True:
        bot.register_next_step_handler(message, set_city)
    else:
        bot.register_next_step_handler(message, by_regex)

def set_city(message):
    bot.send(message, f"✨'{message.text}' set!")
    userLocation = [message.text.split(', ')[0], message.text.split(', ')[1]]
    userBase[message.chat.id] = userLocation

def by_regex(message): # if the city sent by user is incorrect by regex
    bot.send_message(message.chat.id, f"😔What you've sent us does not follow the example, try again") # rewrite so we can ask again



@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    weather = get_current_weather(userBase[message.chat.id][0], userBase[message.chat.id][1])
    bot.send_message(message.chat.id, weather)


bot.polling()






