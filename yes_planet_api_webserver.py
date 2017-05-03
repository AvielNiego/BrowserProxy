# coding=utf-8
import datetime
import json
import random
import string

from flask import Flask
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)
driver = None
waiter = None


def create_new_driver():
    global driver, waiter
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    waiter = WebDriverWait(driver, 10, 0.1)
    driver.get("http://www.yesplanet.co.il/")
    waiter.until(lambda d: d.find_elements_by_id("fancy_overlay"))


@app.route("/")
def yesplanet_api_home():
    create_new_driver()
    return driver.page_source


@app.route("/presentationsJSON")
def yesplanet_api_presentations():
    return get_yesplanet_path("movies/presentationsJSON")


def get_yesplanet_path(path):
    create_new_driver()
    var_name = ''.join(random.choice(string.ascii_letters) for _ in range(15))
    driver.execute_script('%s = null' % var_name)
    driver.execute_script(
        ("$.ajax({'url' : '%s','type' : 'GET','success' : function(data) {" + var_name + " = data}});") % path)
    waiter.until(lambda d: d.execute_script("return %s != null" % var_name))
    return json.dumps(driver.execute_script("return %s" % var_name))


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    create_new_driver()
    app.run('0.0.0.0')
