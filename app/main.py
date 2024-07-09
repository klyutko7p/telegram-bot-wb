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
# chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

driver = webdriver.Chrome(options=chrome_options)
print("Браузер успешно открыт")

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home_view():
    return "<h1>Welcome to Geeks for Geeks</h1>"

@app.route('/post_endpoint', methods=['POST'])
def handle_post():
    url = request.json['url']
    print(url)

    driver.get(url)

    try:
        price_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "ins"))
        )

        price = price_element.text


    except Exception as e:
        print("Ошибка при поиске заголовка страницы:", e)
        return None

    response_data = {'status': 'success', 'message': f'{price}'}
    return jsonify(response_data)