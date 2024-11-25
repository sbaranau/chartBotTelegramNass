import logging

import telebot
from telebot import types
import data  # Import the menu structure
from gpt import GPT
import configparser

logging.basicConfig(level=logging.INFO)

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the properties file
config.read("config.ini")

# Access values
api_key = config["DEFAULT"]["api_key"]
gpt = GPT(api_key)

chunk_size = int(config["DEFAULT"]["chunk_size"])
chunk_overlap = int(config["DEFAULT"]["chunk_overlap"])
# Initialize the bot with your token
bot_key=config["DEFAULT"]["bot_key"]
bot = telebot.TeleBot(bot_key)

backButton = types.KeyboardButton('Главное меню')
bookButton = types.KeyboardButton('📝 Записаться')

btn1 = types.KeyboardButton("👩‍💼 Обо мне")
btn2 = types.KeyboardButton("📦 Мои продукты")
btn3 = types.KeyboardButton("📜 Мои сертификаты")
btn4 = types.KeyboardButton("💬 Отзывы")
btn5 = types.KeyboardButton("📞 Контакт")

btn11 = types.KeyboardButton('🆓 Бесплатная диагностическая консультация')
btn21 = types.KeyboardButton('⚙️Разовая коуч-сессия')
btn31 = types.KeyboardButton('🎯 Стратегическая сессия')
btn41 = types.KeyboardButton('✅ Пакеты Коуч-сессий')
btn51 = types.KeyboardButton('🎴 Коуч-сессия с МАК-картами')
btn61 = types.KeyboardButton('🎲 Игра Лила')

@bot.message_handler(commands=['start']) #стартовая команда
def start(message):
    # Стартовое меню
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2, btn3, btn5)
    send_message = f'<b>Привет {message.from_user.first_name} </b> {data.initial_question}\n\n Выберите раздел, который Вас интересует:'
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    final_message = "" # Переменная для финального сообщения после обработки
    # get_message_bot = message.text.strip().lower() # Считывает ввод в нижнем регистре

    # Стартовое меню для RU
    if message.text.endswith('Обо мне'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 3)
        markup.add(backButton)
        bot.send_message(message.from_user.id, "👋 Привет!", reply_markup=markup, parse_mode='Markdown')
        bot.send_message(message.from_user.id, data.data['About Me'], reply_markup=markup, parse_mode='Markdown')
        bot.send_message(message.from_user.id, data.data['My_goals'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Мои продукты'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn11)
        markup.add(btn21)
        markup.add(btn31)
        markup.add(btn41)
        markup.add(btn51)
        markup.add(btn61)
        markup.add(backButton)
        bot.send_message(message.from_user.id, data.data['Menu_services'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Бесплатная диагностическая консультация'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(bookButton, btn2, backButton)
        bot.send_message(message.from_user.id, data.data['free_diag'], reply_markup=markup,parse_mode='Markdown')

    elif message.text.endswith('Разовая коуч-сессия'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(bookButton, btn2, backButton)
        bot.send_message(message.from_user.id, data.data['single_coach'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Стратегическая сессия'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(bookButton, btn2, backButton)
        bot.send_message(message.from_user.id, data.data['strateg_session'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Пакеты Коуч-сессий'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(bookButton, btn2, backButton)
        bot.send_message(message.from_user.id, data.data['coach_pack'], reply_markup=markup,parse_mode='Markdown')

    elif message.text.endswith('Коуч-сессия с МАК-картами'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(bookButton, btn2, backButton)
        bot.send_message(message.from_user.id, data.data['mac_cart'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Игра Лила'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(bookButton, btn2, backButton)
        bot.send_message(message.from_user.id, data.data['lila'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Главное меню') or message.text == "" or not message.text.strip():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn1, btn2, btn3, btn5)
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню.', reply_markup=markup, parse_mode='Markdown')


    elif message.text.endswith('Отзывы'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.from_user.id, "Ok", reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Мои сертификаты'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(backButton)
        for url in data.image_urls:
            bot.send_photo(message.chat.id, url, caption="Еще сертификат )", reply_markup=markup, parse_mode='Markdown')


    elif message.text.endswith('Записаться') or message.text.endswith('Контакт'):
    # Create an inline keyboard
        markup = types.InlineKeyboardMarkup()
        # Add buttons with proper URLs
        markup.add(types.InlineKeyboardButton("WhatsApp", url="https://wa.me/48662416067"))  # Replace with your phone number
        markup.add(types.InlineKeyboardButton("Telegram", url="https://t.me/Nastassia_Baranava"))  # Replace with your username
        markup.add(types.InlineKeyboardButton("Instagram", url="https://www.instagram.com/nastassia.baranava/"))  # Replace with your username
        markup.add(types.InlineKeyboardButton("Главное меню", callback_data="Главное меню"))

        # Send the message with the inline keyboard
        bot.send_message(
            message.chat.id,
            "📩 Выберите вариант, чтобы связаться со мной:",
            reply_markup=markup
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn1, btn2, btn3, btn5)
        answer = gpt.ask_chart_gpt(message.text)
        bot.send_message(message.from_user.id, answer, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "Главное меню")
def handle_back_to_main_menu(call):
    # Back to the main menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn1, btn2, btn3, btn5)
    bot.send_message(call.message.chat.id, "Вы вернулись в главное меню.", reply_markup=markup)


# Отправка final_message
#bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)

if __name__ == "__main__":
    logging.info("Start init gpt chart and parse file with data")
    gpt.init_bot(chunk_size, chunk_overlap)
    logging.info("BOT started")
    bot.polling(none_stop=True)
