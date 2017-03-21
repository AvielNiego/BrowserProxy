import time

from flask import Flask
from flask import request
from pyvirtualdisplay import Display
from selenium import webdriver

app = Flask(__name__)
display = Display(visible=0, size=(800, 600))
display.start()


@app.route("/")
def yesplanet_api():
    return "Hi"


@app.route("/yesplanet/api")
def yesplanet_api():
    driver = webdriver.Firefox()
    driver.get(request.args.get('url'))
    time.sleep(5)
    source = driver.page_source
    driver.close()
    return source
