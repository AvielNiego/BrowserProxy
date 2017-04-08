# coding=utf-8
import time

from flask import Flask
from flask import request
from pyvirtualdisplay import Display
from selenium import webdriver

app = Flask(__name__)


@app.route("/")
def hello():
    return "שלום"


def create_new_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(chrome_options=chrome_options)


@app.route("/yesplanet/api")
def yesplanet_api():
    driver = create_new_driver()
    driver.get(request.args.get('url'))
    time.sleep(5)
    source = driver.page_source
    driver.close()
    return source


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    app.run('0.0.0.0')
