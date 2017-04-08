# coding=utf-8
import json

import datetime
from flask import Flask
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)
last_updated = datetime.datetime.now()
presentations_json = {}


def create_new_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(chrome_options=chrome_options)


@app.route("/yesplanet/api/presentations")
def yesplanet_api_presentations():
    if datetime.datetime.now() - datetime.timedelta(hours=1) > last_updated:
        update_presentations_json()
    return presentations_json


def update_presentations_json():
    global presentations_json, last_updated
    driver = create_new_driver()
    waiter = WebDriverWait(driver, 10, 0.001)
    driver.get("http://www.yesplanet.co.il/")
    waiter.until(lambda d: d.find_elements_by_id("fancy_overlay"))
    driver.execute_script(
        "$.ajax({'url' : 'movies/presentationsJSON','type' : 'GET','success' : function(data) {a = data}});")
    waiter.until(lambda d: d.execute_script("return typeof a !== 'undefined'"))
    presentations_json = json.dumps(driver.execute_script("return a"))
    last_updated = datetime.datetime.now()
    driver.close()
    return presentations_json


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    app.run('0.0.0.0')
