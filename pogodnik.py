import json
import telebot
from telebot import types
import requests as req
from geopy import geocoders
import datetime
import time


""" Токен тг бота """

token = '5428906787:AAF8snYeonh9EfQd07lJy8NdmGW8Q8fQaLo'


""" Токен api accuweather """

# token_accu = 'qG1XxS0aiZ2Lv9WB7nbknPjARWxhAykY'
# token_accu = 'rSv5RFS4giNPARr6JxVSMTS5SAKd3B17'
token_accu ='HPdkcAHYdVZBpTtPDOLpgDRGTr8FteQK'


""" Токен api yandex """

token_yandex = '2c20ad38-27ba-4070-9633-74d07bdac1ea'




""" Код локации """

def code_location(latitude: str, longitude: str, token_accu: str):
    url_location_key = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' \
                       f'{token_accu}&q={latitude},{longitude}&language=ru'
    print(url_location_key)
    resp_loc = req.get(url_location_key, headers={"APIKey": token_accu})
    json_data = json.loads(resp_loc.text)
    print(json_data)
    code = json_data['Key']
    return code


""" Определение города по долготе и широте """

def city_location(latitude: str, longitude: str, token_accu: str):
    url_location_key = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' \
                       f'{token_accu}&q={latitude},{longitude}&language=ru'
    print(url_location_key)
    resp_loc = req.get(url_location_key, headers={"APIKey": token_accu})
    json_data = json.loads(resp_loc.text)
    print(json_data)
    code = json_data['LocalizedName']
    print(code)
    return code


""" Определение погоды """

def weather(code_loc: str, token_accu: str):
    url_weather = f'http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{code_loc}?' \
                  f'apikey={token_accu}&language=ru&metric=True'
    response = req.get(url_weather, headers={"APIKey": token_accu})
    json_data = json.loads(response.text)
    dict_weather = dict()
    dict_weather['link'] = json_data[0]['MobileLink']
    time = 'сейчас'
    dict_weather[time] = {'temp': json_data[0]['Temperature']['Value'], 'sky': json_data[0]['IconPhrase']}
    for i in range(1, len(json_data)):
        time = 'через' + str(i) + 'ч'
        dict_weather[time] = {'temp': json_data[i]['Temperature']['Value'], 'sky': json_data[i]['IconPhrase']}
    return dict_weather


""" Советы по погоде """

def advice(temp):
    if temp < -30:
        return 'Если ты думаешь, что погулять - это отличная идея, сделай себе горячий чай и подумай еще раз'
    elif -30 <= temp < -20:
        return 'Как хорошо, что ты программист и можешь сидеть дома'
    elif -20 <= temp < -10:
        return 'Если ты неходячая тепло-энергостанция, то хотя - бы надень шарф '
    elif -10 <= temp < 0:
        return 'Белая обувь - не лучший выбор, ведь снежная слякоть оставит напоминание о себе. И не забудь, что сейчас лучшее время, чтобы сделать снеговика'
    elif 0 <= temp < 10:
        return 'Не забудь зонтик, ведь в такую погоду дождь может быть особенно неприятным'
    elif 10 <= temp < 20:
        return 'Забудь о зимнем пуховике, деревья цветут, а погода дает тебе возможность расцвести вместе с ними'
    elif 20 <= temp < 30:
        return 'Отличная погода для прогулки в легкой одежде, но не забудь взять с собой холодный напиток'
    elif temp >= 30:
        return 'ммм.. А где здесь ближайшая морозильная камера?'


"""Вывод погоды"""

def print_weather(dict_weather, message):
    print(dict_weather)
    sov = advice(dict_weather["сейчас"]["temp"])
    bot.send_message(message.from_user.id,
                                           f'{advice(dict_weather["сейчас"]["temp"])}\n'
                                           f' Температура сейчас {dict_weather["сейчас"]["temp"]}!\n'
                                           f' А на небе {dict_weather["сейчас"]["sky"]}.\n'
                                           f' Температура через три часа {dict_weather["через3ч"]["temp"]}!\n'
                                           f' А на небе {dict_weather["через3ч"]["sky"]}.\n'
                                           f' Температура через шесть часов {dict_weather["через6ч"]["temp"]}!\n'
                                           f' А на небе {dict_weather["через6ч"]["sky"]}.\n'
                                           f' Температура через девять часов {dict_weather["через9ч"]["temp"]}!\n'
                                           f' А на небе {dict_weather["через9ч"]["sky"]}.\n')
    bot.send_message(message.from_user.id, f' А здесь ссылка на подробности '
                                           f'{dict_weather["link"]}')


## Вывод погоды, только платформа яндекс ##

def print_yandex_weather(dict_weather_yandex, message):
    day = {'night': 'ночью', 'morning': 'утром', 'day': 'днем', 'evening': 'вечером', 'fact': 'сейчас'}
    bot.send_message(message.from_user.id, f'А яндекс говорит:')
    for i in dict_weather_yandex.keys():
        if i != 'link':
            time_day = day[i]
            bot.send_message(message.from_user.id, f'Температура {time_day} {dict_weather_yandex[i]["temp"]}'
                                                   f', на небе {dict_weather_yandex[i]["condition"]}')

    bot.send_message(message.from_user.id, f' А здесь ссылка на подробности '
                                           f'{dict_weather_yandex["link"]}')


""" Определение геопозиции по городу """

def geo_pos(city: str):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude


""" Определение погоды Яндекс """
def yandex_weather(latitude, longitude, token_yandex: str):
    url_yandex = f'https://api.weather.yandex.ru/v2/informers/?lat={latitude}&lon={longitude}&[lang=ru_RU]'
    print(url_yandex)
    yandex_req = req.get(url_yandex, headers={'X-Yandex-API-Key': token_yandex}, verify=False)
    print(yandex_req)

    conditions = {'clear': 'ясно', 'partly-cloudy': 'малооблачно', 'cloudy': 'облачно с прояснениями',
                  'overcast': 'пасмурно', 'drizzle': 'морось', 'light-rain': 'небольшой дождь',
                  'rain': 'дождь', 'moderate-rain': 'умеренно сильный', 'heavy-rain': 'сильный дождь',
                  'continuous-heavy-rain': 'длительный сильный дождь', 'showers': 'ливень',
                  'wet-snow': 'дождь со снегом', 'light-snow': 'небольшой снег', 'snow': 'снег',
                  'snow-showers': 'снегопад', 'hail': 'град', 'thunderstorm': 'гроза',
                  'thunderstorm-with-rain': 'дождь с грозой', 'thunderstorm-with-hail': 'гроза с градом'
                  }
    wind_dir = {'nw': 'северо-западное', 'n': 'северное', 'ne': 'северо-восточное', 'e': 'восточное',
                'se': 'юго-восточное', 's': 'южное', 'sw': 'юго-западное', 'w': 'западное', 'с': 'штиль'}


    yandex_json = json.loads(yandex_req.text)
    print(yandex_json)
    yandex_json['fact']['condition'] = conditions[yandex_json['fact']['condition']]
    yandex_json['fact']['wind_dir'] = wind_dir[yandex_json['fact']['wind_dir']]
    for parts in yandex_json['forecast']['parts']:
        parts['condition'] = conditions[parts['condition']]
        parts['wind_dir'] = wind_dir[parts['wind_dir']]


    weather = dict()
    params = ['condition', 'wind_dir', 'pressure_mm', 'humidity']
    for parts in yandex_json['forecast']['parts']:
        weather[parts['part_name']] = dict()
        weather[parts['part_name']]['temp'] = parts['temp_avg']
        for param in params:
            weather[parts['part_name']][param] = parts[param]

    weather['fact'] = dict()
    weather['fact']['temp'] = yandex_json['fact']['temp']
    for param in params:
        weather['fact'][param] = yandex_json['fact'][param]

    weather['link'] = yandex_json['info']['url']
    return weather


""" Добавление города """
def add_city(message):
    try:
        latitude, longitude = geo_pos(message.text.lower().split('город ')[1])
        global cities
        cities[message.from_user.id] = message.text.lower().split('город ')[1]
        with open('cities.json', 'w') as f:
            f.write(json.dumps(cities))
        return cities, 0
    except Exception as err:
        return cities, 1


""" Вкл/Выкл уведомления """

def notice(On_Off, count):
    if On_Off == 0 and count == 0:
        return 'Выкл'
    elif On_Off == 1 and count == 0:
        return 'Вкл'
    elif On_Off == 0 and count == 1:
        return 1
    elif On_Off == 1 and count == 1:
        return 0


bot = telebot.TeleBot(token)


""" Cities используется для определения стандартного города """

with open('cities.json', encoding='utf-8') as f:
    cities = json.load(f)


""" Старт бота """

@bot.message_handler(command=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("👋 Поздороваться")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    markup.add(btn1, btn2)
    bot.reply_to(message, f'Я погодабот, приятно познакомитсья, {message.from_user.first_name}', reply_markup=markup)


""" Все исходы при отправлении текста пользователем """

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global cities

    if message.text == '/start':
        """
        Начало бота и приветствие
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("👋 Поздороваться")
        markup.add(btn1)
        bot.reply_to(message, f'Я погодабот, приятно познакомиться, {message.from_user.first_name})',
                     reply_markup=markup)


    elif message.text.lower() == "👋 поздороваться" or message.text.lower() == 'привет':
        """
        Начальное меню
        Добавлены кнопки для управления нашим ботом
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("Погода🌤")
        b2 = types.KeyboardButton("Уведомления🔔")
        b3 = types.KeyboardButton("Поддержка⚙️")
        markup.add(b1, b2, b3)
        bot.send_message(message.from_user.id,
                         f' Добрый день, {message.from_user.first_name}! Позвольте Я доложу '
                         f' Вам о погоде! Нажмите кнопку "погода" и я напишу погоду в Вашем'
                         f' "стандартном" городе или напишите название города в котором Вы сейчас', reply_markup=markup)


    elif message.text.lower() == "поддержка⚙️":
        """
        Связь с разработчиком
        """
        bot.send_message(message.from_user.id,
                         f'Если у вас возникли вопросы, то можете написать сюда:\n'
                         f'@timergal1 @ilyakazankov @KekJloXopPonNbi')


    elif message.text.lower() == "меню📜" or message.text.lower() == "меню":
        """
        Основное меню
        Отличие от начального меню в том, что текст от нашего бота другой
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("Погода🌤")
        b2 = types.KeyboardButton("Уведомления🔔")
        b3 = types.KeyboardButton("Поддержка⚙️")
        markup.add(b1, b2, b3)
        bot.send_message(message.from_user.id,f'Жду приказов!',
                     reply_markup=markup)


    elif message.text.lower() == 'погода🌤' or message.text.lower() == 'погода':
        """
        Погода
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        b1 = types.KeyboardButton("Меню📜")
        markup.add(b1)


        if message.from_user.id in cities.keys():
            """
            Берем наш стандартный город и выводим погоду
            """
            city = cities[message.from_user.id]
            bot.send_message(message.from_user.id, f' Сейчас все доложу, {message.from_user.first_name}!'
                                                   f' Твой город {city}', reply_markup=markup)
            latitude, longitude = geo_pos(city)
            code_loc = code_location(latitude, longitude, token_accu)
            you_weather = weather(code_loc, token_accu)
            print_weather(you_weather, message)
            # yandex_weather_x = yandex_weather(latitude, longitude, token_yandex)
            # print_yandex_weather(yandex_weather_x, message)


        else:
            """
            Если у нас нет стандартного города, 
            то спрашиваем у пользователя его город
            """
            b1 = types.KeyboardButton("Отправить местоположение📍")
            markup.add(b1)
            bot.send_message(message.from_user.id, f' {message.from_user.first_name}!'
                                                   f' Я не знаю Ваш город! Просто напиши:'
                                                   f'"Мой город *****" и я запомню твой стандартный город!'
                                                   f'Или отправь гео)', reply_markup=markup)


    elif message.text.lower() == 'уведомления🔔':
        """
        Уведомления, 
        то есть каждый день в определенное время будет присылаться погода
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вкл уведомления🔔")
        btn2 = types.KeyboardButton("Задать время🕞")
        btn3 = types.KeyboardButton("Меню📜")
        markup.add(btn1, btn2, btn3)
        bot.reply_to(message, f'Здесь ты сможешь управлять уведомлениями о погоде.',
                     reply_markup=markup)


    elif message.text.lower() == 'задать время🕞':
        """
        Задаем время,
        в которое нам будет приходить уведомления о погоде
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(f'Вкл уведомления🔔')
        btn2 = types.KeyboardButton("Задать время🕞")
        btn3 = types.KeyboardButton("Меню📜")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id, f'Напиши время, в которое ты хотел бы получать прогноз погоды. Формат должен быть такой, ЧЧ:ММ. Например, 16:45.',
                     reply_markup=markup)


    elif message.text.lower() == 'вкл уведомления🔔':
        """
        Уведомления включены
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(f'Выкл уведомления💤')
        btn2 = types.KeyboardButton("Задать время🕞")
        btn3 = types.KeyboardButton("Меню📜")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id,'Уведомления включены🔔', reply_markup=markup)


    elif message.text.lower() == 'выкл уведомления💤':
        """
        Уведомления выключены
        """
        # On_Off = notice(1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton(f'Вкл уведомления🔔')
        btn2 = types.KeyboardButton("Задать время🕞")
        btn3 = types.KeyboardButton("Меню📜")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.from_user.id,'Уведомления выключены💤', reply_markup=markup)


    elif message.text.lower()[:9] == 'мой город':
        """
        Добавление стандартного города
        """
        cities, flag = add_city(message)
        if flag == 0:
            bot.send_message(message.from_user.id, f' {message.from_user.first_name}!'
                                                   f' Теперь я знаю Ваш город! это'
                                                   f' {cities[message.from_user.id]}')


        else:
            bot.send_message(message.from_user.id, f' {message.from_user.first_name}!'
                                                   f' Что то пошло не так :(')


    elif message.text[2:3] == ':' and len(message.text) == 5:
        """
        Задается время, в которое будет отправляться погода
        """
        HH = int(message.text[0:2])
        MM = int(message.text[3:5])
        print(HH, MM)
        bot.reply_to(message, f'Отлично! Время установлено!')

    elif message.text == 'Отправить местоположение📍':
        """
        Отправляем геолокацию
        """
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_geo = types.KeyboardButton(text="Отправить местоположение📍", request_location=True)
        btn = types.KeyboardButton(text="Меню📜")
        keyboard.add(button_geo, btn)
        bot.send_message(message.chat.id, "Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)
    # elif:
    #
    else:

        try:
            city = message.text
            bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}! Твой город {city}')
            latitude, longitude = geo_pos(city)
            code_loc = code_location(latitude, longitude, token_accu)
            you_weather = weather(code_loc, token_accu)
            print_weather(you_weather, message)
            # yandex_weather_x = yandex_weather(latitude, longitude, token_yandex)
            # print_yandex_weather(yandex_weather_x, message)


        except AttributeError as err:
            bot.send_message(message.from_user.id, f'{message.from_user.first_name}!'
                                                   f'Я не нашел такого города!'
                                                   f'И получил ошибку {err}, попробуй другой город')

""" Случай при отправлении пользователем локации """

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        """
        Пользователь отправиль гео, 
        и данные идут на обработку
        """

        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        f = open("location.txt", 'w')
        lat = message.location.latitude
        lon = message.location.longitude
        f.write(str(lat))
        f.write(' ')
        f.write(str(lon))
        # city = city_location(lon, lon, token_accu)
        bot.send_message(message.from_user.id, f'А вот и погода, {message.from_user.first_name}!')
        # latitude, longitude = geo_pos(city)
        code_loc = code_location(lat, lon, token_accu)
        you_weather = weather(code_loc, token_accu)
        print_weather(you_weather, message)
        # print(city)
        # bot.send_message(message.from_user.id, f'Твой город {city}?')


bot.polling()
# now = datetime.datetime.now()
# current_time = now.strftime("%H:%M")
# while True:
#     time.sleep(1)
#     if current_time == '23:11':#Выставляете ваше время
#         print('pass')
#         bot.send_message("тут айди вашей группы", 'text')
On_Off = 0

""" Запускаем бота """

bot.polling(none_stop=True)