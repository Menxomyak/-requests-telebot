import telebot
import requests
from datetime import datetime

TOKEN = '7025577959:AAFElXEj3TO8ZskYHS4IsxJv1p76qV5XV64'

API_KEY = '8aa247817df42445963ae207d9ceec0c'

URL = "http://api.openweathermap.org/data/2.5/weather"

bot = telebot.TeleBot(TOKEN)

# /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я могу показать тебе текущую погоду в любом городе. Просто отправь мне название города.")

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    city_name = message.text.strip()
    
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    response = requests.get(URL, params=params)
    
    if response.status_code == 200:
        weather_data = response.json()
        
        temperature = weather_data['main']['temp']
        vlaga = weather_data['main']['vlaga']
        description = weather_data['weather'][0]['description'].capitalize()
        
        # ответ
        answer = f"Текущая погода в {city_name}:\nТемпература: {temperature}°C\nВлажность: {vlaga}%\nОписание: {description}"
        
        # сохранение в бд
        save_weather_request(city_name, message.from_user.id, temperature, vlaga, description)
        
        bot.reply_to(message, answer)
    else:
        bot.reply_to(message, "Не удалось получить данные о погоде. Проверьте правильность названия города и попробуйте снова.")

# история
def save_weather_request(city, user_id, temp, vlagaid, desc):
    # запись в бд
    print(f"{datetime.now()} | Пользователь {user_id} запросил погоду для города {city}: температура {temp}, влажность {vlagaid}, описание {desc}")

if __name__ == '__main__':
    bot.polling(none_stop=True)
