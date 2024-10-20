import telebot
from telebot import types
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Инициализация бота и базы данных
API_TOKEN = '8042922987:AAEj2JMryWZcJxE1p1vTqWisjcGFpe6komI'
DATABASE_URL = 'mysql+pymysql://root@localhost:3308/Mail_DNR'

bot = telebot.TeleBot(API_TOKEN)

# Настройка SQLAlchemy
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Определение моделей базы данных
class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

class Talon(Base):
    __tablename__ = 'talon'
    talon_number = Column(Integer, primary_key=True)
    date_talon = Column(DateTime, nullable=False)
    phone_number = Column(String(15), nullable=False)
    servicesid = Column(Integer, ForeignKey('services.id'), nullable=False)
    completed = Column(Boolean, default=False)
    service = relationship('Service')

# Храним выбор пользователя (дата, время и услуга) для завершения регистрации
user_data = {}

# Запрос номера телефона
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Поделиться номером телефона", request_contact=True)
    markup.add(button_phone)
    bot.send_message(message.chat.id, "Привет! Поделитесь, пожалуйста, вашим номером телефона.", reply_markup=markup)

# Обработка контакта и выбор услуги
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    phone_number = message.contact.phone_number
    user_data[message.chat.id] = {'phone_number': phone_number}  # Сохраняем номер телефона
    bot.send_message(message.chat.id, f"Ваш номер телефона: {phone_number}")
    
    # Создание кнопок выбора услуги
    markup = types.InlineKeyboardMarkup()
    services = session.query(Service).all()
    for service in services:
        markup.add(types.InlineKeyboardButton(service.name, callback_data=f'service_{service.id}'))
    
    bot.send_message(message.chat.id, "Теперь выберите услугу:", reply_markup=markup)

# Обработка выбора услуги
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def process_service(call):
    service_id = int(call.data.split('_')[1])
    user_data[call.message.chat.id]['service_id'] = service_id  # Сохраняем выбранную услугу
    
    # Проверяем, есть ли подуслуги для выбранной услуги
    if service_id in [1, 2, 3, 4]:  # Услуги с подуслугами
        markup = types.InlineKeyboardMarkup()
        
        if service_id == 1:  # Услуга 1: "Отправить письма", "Отправить посылки", "Получить отправления"
            sub_services = ['Отправить письма', 'Отправить посылки', 'Получить отправления']
        elif service_id == 2:  # Услуга 2: "Отправить переводы", "Получить переводы"
            sub_services = ['Отправить переводы', 'Получить переводы']
        elif service_id == 3:  # Услуга 3: "Коммунальные услуги", "Интернет платежи", "Телефония"
            sub_services = ['Коммунальные услуги', 'Интернет платежи', 'Телефония']
        elif service_id == 4:  # Услуга 4: "Купить стартовые пакеты", "Восстановить sim-карты", "Купить sim-карты"
            sub_services = ['Купить стартовые пакеты', 'Восстановить sim-карты', 'Купить sim-карты']

        for sub_service in sub_services:
            markup.add(types.InlineKeyboardButton(sub_service, callback_data=f'subservice_{sub_service}'))

        bot.send_message(call.message.chat.id, "Теперь выберите подуслугу:", reply_markup=markup)
    else:
        # Если подуслуги нет, продолжаем с выбором даты
        bot.send_message(call.message.chat.id, "Теперь выберите дату:", reply_markup=create_date_time_buttons())

# Обработка выбора подуслуги
@bot.callback_query_handler(func=lambda call: call.data.startswith('subservice_'))
def process_subservice(call):
    subservice_name = call.data.split('_')[1]
    user_data[call.message.chat.id]['subservice'] = subservice_name  # Сохраняем выбранную подуслугу
    bot.send_message(call.message.chat.id, f"Вы выбрали подуслугу: {subservice_name}")
    
    # Переходим к выбору даты
    bot.send_message(call.message.chat.id, "Теперь выберите дату:", reply_markup=create_date_time_buttons())

    
    # Создание кнопок для выбора даты
  

# Создание кнопок для выбора даты на +- 8 дней
def create_date_time_buttons():
    markup = types.InlineKeyboardMarkup()
    today = datetime.date.today()
    for i in range(9):  # Дата с диапазоном на 8 дней вперед
        date_str = (today + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        markup.add(types.InlineKeyboardButton(date_str, callback_data=f'date_{date_str}'))
    return markup

# Храним выбор пользователя (дата, время и услуга) для завершения регистрации
user_data = {}

# Создание кнопок для выбора часовых интервалов (10:00–11:00, 11:00–12:00 и т.д.)
def create_hour_buttons():
    markup = types.InlineKeyboardMarkup(row_width=3)  # В ряд добавляем 3 кнопки
    start_time = datetime.time(10, 0)  # Начало с 10:00
    end_time = datetime.time(18, 0)  # Конец в 18:00
    current_time = datetime.datetime.combine(datetime.date.today(), start_time)

    while current_time.time() < end_time:
        next_time = (current_time + datetime.timedelta(hours=1)).strftime('%H:%M')
        time_str = f"{current_time.strftime('%H:%M')} - {next_time}"
        markup.add(types.InlineKeyboardButton(time_str, callback_data=f'hour_{current_time.strftime("%H")}'))
        current_time += datetime.timedelta(hours=1)

    return markup

# Обработка выбора часового интервала
@bot.callback_query_handler(func=lambda call: call.data.startswith('hour_'))
def process_hour(call):
    hour_str = call.data.split('_')[1]
    user_data[call.message.chat.id]['hour'] = hour_str  # Сохраняем выбранный час
    bot.send_message(call.message.chat.id, f"Вы выбрали интервал: {hour_str}:00 - {int(hour_str) + 1}:00")

    # Показать кнопки с минутами для выбранного часа
    bot.send_message(call.message.chat.id, "Теперь выберите точное время:", reply_markup=create_minute_buttons(hour_str))

# Создание кнопок для выбора минут (с шагом в 15 минут) внутри выбранного часа
def create_minute_buttons(selected_hour):
    markup = types.InlineKeyboardMarkup(row_width=4)  # В ряд добавляем 4 кнопки
    selected_hour = int(selected_hour)
    start_time = datetime.time(selected_hour, 0)  # Начало выбранного часа (например, 10:00)
    end_time = datetime.time(selected_hour + 1, 0)  # Конец выбранного часа (например, 11:00)
    current_time = datetime.datetime.combine(datetime.date.today(), start_time)

    while current_time.time() < end_time:
        time_str = current_time.strftime('%H:%M')
        markup.add(types.InlineKeyboardButton(time_str, callback_data=f'minute_{time_str}'))
        current_time += datetime.timedelta(minutes=15)  # Шаг 15 минут

    return markup

# Обработка выбора времени и регистрация талона
@bot.callback_query_handler(func=lambda call: call.data.startswith('minute_'))
def process_minute(call):
    time_str = call.data.split('_')[1]
    user_data[call.message.chat.id]['time'] = time_str  # Сохраняем выбранное точное время

    try:
        # Формируем полную дату и время
        chosen_date = user_data[call.message.chat.id]['date']
        chosen_time = user_data[call.message.chat.id]['time']
        datetime_talon = datetime.datetime.strptime(f"{chosen_date} {chosen_time}", '%Y-%m-%d %H:%M')

        # Сохранение талона в базу данных
        talon = Talon(
            date_talon=datetime_talon,
            phone_number=user_data[call.message.chat.id]['phone_number'],
            servicesid=user_data[call.message.chat.id]['service_id']
        )
        session.add(talon)
        session.commit()

        # Получаем номер талона
        talon_number = talon.talon_number

        # Ответ пользователю
        bot.send_message(call.message.chat.id, f"Талон зарегистрирован на время: {chosen_time}, дата: {chosen_date}. Ваш номер талона: {talon_number}. Спасибо!")

    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка при регистрации талона: {str(e)}")

# Обработка выбора даты
@bot.callback_query_handler(func=lambda call: call.data.startswith('date_'))
def process_date(call):
    date_str = call.data.split('_')[1]
    user_data[call.message.chat.id]['date'] = date_str  # Сохраняем выбранную дату
    bot.send_message(call.message.chat.id, f"Вы выбрали дату: {date_str}")
    
    # Показать кнопки выбора часового интервала
    bot.send_message(call.message.chat.id, "Теперь выберите интервал времени:", reply_markup=create_hour_buttons())


if __name__ == '__main__':
    bot.polling(none_stop=True)
