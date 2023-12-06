import subprocess

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def check():
    try:
        with requests.get("http://127.0.0.1:9222/", timeout=0.1) as resp:
            if resp.status_code == 200:
                return True
    except:
        pass
    return False


def start():
    if not check():
        subprocess.Popen('sudo /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222', shell=True)
    options = Options()
    options.debugger_address = '127.0.0.1:9222'
    driver = webdriver.Chrome(options=options)
    return driver


driver = start()
driver.get("https://www.baidu.com")
print(11)
