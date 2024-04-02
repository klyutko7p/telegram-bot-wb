import re

from httpcore import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telebot import TeleBot
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

driver = webdriver.Chrome(options=chrome_options)
print("Браузер успешно открыт")

# Функция для открытия браузера и выполнения процедуры
def open_browser_and_process(url):
    # Открытие веб-страницы
    driver.get(url)

    # Явное ожидание загрузки элемента с классом "price-block__final-price.wallet"
    try:
        elem = WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "price-block__final-price.wallet"))
        )
    except TimeoutException:
        print("Время ожидания истекло. Элемент не найден.")
        return None

    # Извлечение текста элемента
    text = elem.text

    # Возвращаем извлеченный текст
    return text


# Инициализация бота
bot = TeleBot('7185448364:AAFKMQUW1Z6_oJcOYnK8MxTbSLES-yiDlK0')


# Обработчик команды '/start'
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
                     "Привет! Отправь мне сообщение с текстом '/get_price [ссылка]', чтобы получить цену товара.")


# Обработчик команды '/get_price'
@bot.message_handler(commands=['get_price'])
def handle_get_price(message):
    # Получаем текст сообщения пользователя
    text = message.text

    # Проверяем, содержит ли сообщение ссылку
    url_match = re.search(r'(https?://\S+)', text)
    if url_match:
        url = url_match.group(1)  # Извлекаем ссылку из сообщения
        # Открываем браузер и получаем цену товара
        text = open_browser_and_process(url)
        if text:
            bot.send_message(message.chat.id, f"Цена товара: {text}")
        else:
            bot.send_message(message.chat.id, "Не удалось получить цену товара.")
    else:
        bot.send_message(message.chat.id,
                         "Не найдена ссылка на товар. Пожалуйста, отправьте ссылку в формате: /get_price [ссылка]")


# Обработчик ошибочных команд
@bot.message_handler(func=lambda message: True)
def handle_invalid(message):
    bot.reply_to(message, "Неизвестная команда. Используйте '/start' для начала.")


@bot.message_handler(commands=['check_browser'])
def handle_check_browser(message):
    driver.get("https://www.python.org")
    title = driver.title
    bot.send_message(message.chat.id, f"Заголовок страницы Python.org: {title}")


# Запуск бота
bot.polling()
