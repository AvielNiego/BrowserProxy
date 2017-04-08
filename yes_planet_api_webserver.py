# coding=utf-8
import json

import datetime
from flask import Flask
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)


def create_new_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(chrome_options=chrome_options)

@app.route("/")
def yesplanet_api_presentations():
    driver = create_new_driver()
    driver.get("http://www.yesplanet.co.il/")
    WebDriverWait(driver, 10, 0.001).until(lambda d: d.find_elements_by_id("fancy_overlay"))
    source = driver.page_source
    driver.close()
    return source


@app.route("/presentationsJSON")
def yesplanet_api_presentations():
    driver = create_new_driver()
    waiter = WebDriverWait(driver, 10, 0.001)
    driver.get("http://www.yesplanet.co.il/")
    waiter.until(lambda d: d.find_elements_by_id("fancy_overlay"))
    driver.execute_script(
        "$.ajax({'url' : 'movies/presentationsJSON','type' : 'GET','success' : function(data) {a = data}});")
    waiter.until(lambda d: d.execute_script("return typeof a !== 'undefined'"))
    presentations_json = json.dumps(driver.execute_script("return a"))
    driver.close()
    return presentations_json


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    app.run('0.0.0.0')
