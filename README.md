# Ben's Weather Bot
## v0.01beta
This monstrosity of a program is my telegram weather bot.
It's currently in beta since it is still relatively raw, so there is room for improvement.

## Commands
- **/set_city** - set your city as a user
- **/get_weather** - output weather in the set by the current user's city
- The user also may send a location as text to get the weather for that specific location.

## What is used in the project
- **TeleBot** - python-telegram integration library *(3rd party library)*
- **SQLite3** - database integration library for saving users' locations
- **Logging** - library for logging errors
- **Indexes (re)** - to check whether or not the user is sending the right thing

## TO-DO
Things to be done:
1. Command buttons;
2. Re-format weather output a different way;
3. Command for user output.

## Deployment

1. Clone the main branch to your local PC.
2. Create a telegram bot with BotFather in Telegram, get an API key
3. [Create an OpenWeatherMap account](https://home.openweathermap.org/users/sign_in), [create & get an API key](https://home.openweathermap.org/api_keys)
4. In the folder with the repository, create a file and call it *apikeys.py*
5. Paste the keys as seen where it says **KEY**:
```
weather_key = 'KEY'
bot_key = 'KEY'
```
6. Run database.py and schema.sql
7. Run main (2).py