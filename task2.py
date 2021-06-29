# Зарегистрироваться на https://openweathermap.org/api и написать функцию,
# которая получает погоду в данный момент для города, название которого получается через input.
# https://openweathermap.org/current

import requests
import os
from dotenv import load_dotenv

load_dotenv('../.env')

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": os.environ.get("key")}
    city_weather = requests.get(base_url, params=params)
    return city_weather.json()

if __name__ == "__main__":
    city = input("Введите название города на английском языке ")
    weather = get_weather(city)
    print(weather)
