import requests
import re 
import apikeys


def get_current_weather(city: str, countryCode: str) -> str:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{countryCode}&appid={apikeys.weather_key}"
    response = requests.get(url)
    weather = response.json()
    if weather == {'cod': '404', 'message': 'city not found'}: # pretty straightforward
        return "City not found"
    
    # forming & styling the string response
    temp = str(int(round(int(weather["main"]["temp"]) - 273.15, 0)))
    if int(temp) > 0:
        temp = "+" + temp + "°"
    else:
        temp = temp + "°"
    
    description = weather['weather'][0]['description']
    styledDesc = rewrittenDescription(description)
    emojiWeather = getEmojiByDescription(description)
    
    
    
    result = f"""Weather in {city} now:
{emojiWeather}{styledDesc}
🌡{temp}"""
    return result


def regex_check(string: str) -> bool:
    pattern = re.compile(r"^[A-Za-z]+, [A-Za-z][A-Za-z]$", re.IGNORECASE) # setting a regex that matches for example: "Moscow, RU"
    return bool(pattern.match(string))


def getEmojiByDescription(desc: str) -> str: # styling
    if desc in emojiDictionary:
        emojiDictionary = {"clear sky": "☀️", "few clouds": "🌤", "scattered clouds": "⛅️", "broken clouds": "⛅️", "shower rain": "🌧", "rain": "🌦", 
                        "thunderstorm": "⛈", "snow": "☃️", "mist": "🌫️", "overcast clouds": "☁️"}
        return emojiDictionary[desc]
    else: return "🌤"

def rewrittenDescription(desc: str) -> str: # styling
    if desc in descDictionary:
        descDictionary = {"clear sky": "Clear sky", "few clouds": "Few clouds", "scattered clouds": "Scattered clouds", "broken clouds": "Broken clouds", "shower rain": "Shower rain", "rain": "Rain", 
                        "thunderstorm": "Thunderstorm", "snow": "Snowy", "mist": "Misty", "overcast clouds": "Cloudy"}
        return descDictionary[desc]
    else:
        descStyled = desc
        descStyled[0] = descStyled[0].capitalize()
        return descStyled
