import logging

import telebot
from telebot import types
import data  # Import the menu structure
from gpt import GPT
import configparser
import os
import sys
import argparse

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

btn_main_menu = types.KeyboardButton('Главное меню')
btn_book = types.KeyboardButton('📝 Записаться')
btn_presents = types.KeyboardButton("🎁 Бонусы")

btn_about_me = types.KeyboardButton("👩‍💼 Обо мне")
btn_my_services = types.KeyboardButton("📦 Мои продукты")
btn_certificates = types.KeyboardButton("📜 Мои сертификаты")
btn_feedbacks = types.KeyboardButton("💬 Отзывы")
btn_contacts = types.KeyboardButton("📞 Контакт")

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
    markup.add(btn_about_me, btn_my_services, btn_certificates, btn_contacts)
    send_message = f'<b>Привет {message.from_user.first_name} </b> {data.initial_question}\n\n Выберите раздел, который Вас интересует:'
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    final_message = "" # Переменная для финального сообщения после обработки
    # get_message_bot = message.text.strip().lower() # Считывает ввод в нижнем регистре

    # Стартовое меню для RU
    if message.text.endswith('Обо мне'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width = 3)
        markup.add(btn_main_menu)
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
        markup.add(btn_main_menu)
        bot.send_message(message.from_user.id, data.data['Menu_services'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Бесплатная диагностическая консультация'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_book, btn_my_services, btn_main_menu)
        bot.send_message(message.from_user.id, data.data['free_diag'], reply_markup=markup,parse_mode='Markdown')

    elif message.text.endswith('Разовая коуч-сессия'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_book, btn_my_services, btn_main_menu)
        bot.send_message(message.from_user.id, data.data['single_coach'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Стратегическая сессия'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_book, btn_my_services, btn_main_menu)
        bot.send_message(message.from_user.id, data.data['strateg_session'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Пакеты Коуч-сессий'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_book, btn_my_services, btn_main_menu)
        bot.send_message(message.from_user.id, data.data['coach_pack'], reply_markup=markup,parse_mode='Markdown')

    elif message.text.endswith('Коуч-сессия с МАК-картами'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_book, btn_my_services, btn_main_menu)
        bot.send_message(message.from_user.id, data.data['mac_cart'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Игра Лила'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_book, btn_my_services, btn_main_menu)
        bot.send_message(message.from_user.id, data.data['lila'], reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Главное меню') or message.text == "" or not message.text.strip():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_about_me, btn_my_services, btn_certificates, btn_presents, btn_contacts)
        bot.send_message(message.from_user.id, 'Вы вернулись в главное меню.', reply_markup=markup, parse_mode='Markdown')


    elif message.text.endswith('Отзывы'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_about_me, btn_my_services, btn_certificates, btn_feedbacks, btn_presents, btn_contacts)
        bot.send_message(message.from_user.id, "Ok", reply_markup=markup, parse_mode='Markdown')

    elif message.text.endswith('Мои сертификаты'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_main_menu)
        for url in data.certificates_image_urls:
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
    elif message.text.endswith('🎁 Бонусы'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_main_menu)
        # Add Google Drive links here

        for present in data.bonus_links:
            bot.send_message(
                message.from_user.id,
                f"{present['name']}\n[Скачать файл]({present['link']})",
                reply_markup=markup,
                parse_mode="Markdown",
        )
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(btn_about_me, btn_my_services, btn_certificates, btn_contacts)
        answer = gpt.ask_chart_gpt(message.text)
        bot.send_message(message.from_user.id, answer, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == "Главное меню")
def handle_back_to_main_menu(call):
    # Back to the main menu
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(btn_about_me, btn_my_services, btn_certificates, btn_contacts)
    bot.send_message(call.message.chat.id, "Вы вернулись в главное меню.", reply_markup=markup)


# Отправка final_message
#bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Logs to console
    ]
)

def setup_file_logging():
    """Configure logging to write to a file."""
    log_file = "bot.log"
    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)


def daemonize():
    """Daemonize the process safely."""
    if os.name != "posix":
        raise NotImplementedError("Daemonization only works on POSIX systems.")

    # Fork once to detach from the controlling terminal
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Parent process exits
    except OSError as e:
        sys.stderr.write(f"Fork failed: {e}\n")
        sys.exit(1)

    # Detach process
    os.setsid()

    # Fork a second time to prevent the daemon from re-acquiring a terminal
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError as e:
        sys.stderr.write(f"Second fork failed: {e}\n")
        sys.exit(1)

    # Redirect standard file descriptors to /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    with open("/dev/null", "rb") as dev_null_in:
        os.dup2(dev_null_in.fileno(), sys.stdin.fileno())
    with open("/dev/null", "wb") as dev_null_out:
        os.dup2(dev_null_out.fileno(), sys.stdout.fileno())
        os.dup2(dev_null_out.fileno(), sys.stderr.fileno())

    # Set up file logging after daemonizing
    setup_file_logging()


def start_bot():
    """Start the bot."""
    logging.info("Start initializing GPT chart and parsing file with data...")
    gpt.init_bot(chunk_size=1024, chunk_overlap=100)
    logging.info("BOT started")
    bot.polling(none_stop=True)


def main():
    # Argument parser
    parser = argparse.ArgumentParser(description="Start the bot.")
    parser.add_argument(
        "--mode",
        choices=["regular", "daemon"],
        default="regular",
        help="Run the bot in 'regular' mode or as a 'daemon'."
    )
    args = parser.parse_args()

    if args.mode == "daemon":
        logging.info("Running the bot in daemon mode...")
        daemonize()
        start_bot()
    else:
        logging.info("Running the bot in regular mode...")
        start_bot()


if __name__ == "__main__":
    main()