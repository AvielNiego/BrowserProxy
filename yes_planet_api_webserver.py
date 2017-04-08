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


@app.route("/yesplanet/api")
def yesplanet_api():
    driver = webdriver.Chrome()
    driver.get(request.args.get('url'))
    time.sleep(5)
    source = driver.page_source
    driver.close()
    return source


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    app.run('0.0.0.0')
