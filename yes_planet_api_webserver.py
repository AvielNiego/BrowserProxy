# coding=utf-8
import json
import random
import string

from flask import Flask
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

app = Flask(__name__)


def create_new_driver():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    waiter = WebDriverWait(driver, 10, 0.1)
    driver.get("http://www.yesplanet.co.il/")
    waiter.until(lambda d: d.find_elements_by_id("fancy_overlay"))
    return driver


@app.route("/")
def yesplanet_api_home():
    driver = create_new_driver()
    try:
        return create_new_driver().page_source
    finally:
        driver.close()


@app.route("/presentationsJSON")
def yesplanet_api_presentations():
    return get_yesplanet_path("movies/presentationsJSON")


def get_yesplanet_path(path):
    var_name = ''.join(random.choice(string.ascii_letters) for _ in range(15))
    driver = create_new_driver()
    driver.execute_script('%s = null' % var_name)
    driver.execute_script(
        ("$.ajax({'url' : '%s','type' : 'GET','success' : function(data) {" + var_name + " = data}});") % path)
    waiter = WebDriverWait(driver, 10, 0.1)
    waiter.until(lambda d: d.execute_script("return %s != null" % var_name))
    result = driver.execute_script("return %s" % var_name)
    driver.close()
    return json.dumps(result)


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 600))
    display.start()
    app.run('0.0.0.0')
