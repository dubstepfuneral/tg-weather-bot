import requests
import re 
import apikeys


def get_current_weather(city, countryCode):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{countryCode}&appid={apikeys.weather_key}"
    response = requests.get(url)
    weather = response.json()
    return f"Weather in {city}, {countryCode.upper()} now: {weather['weather'][0]['description']}"


def regex_check(string):
    print(string)
    pattern = re.compile(r"^[A-Za-z]+, [A-Za-z][A-Za-z]$", re.IGNORECASE) # setting a regex that matches for example: "Moscow, RU"
    return bool(pattern.match(string))