from os import getenv
import threading
import time
from app import app as flask_app
from selenium import webdriver
import requests

BASE_URL = getenv('BASE_URL', 'http://localhost:5000')
WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

def before_all(context):
    context.base_url = BASE_URL
    
    context.server_thread = threading.Thread(
        target=flask_app.run,
        kwargs={'host': '0.0.0.0', 'port': 5000}
    )
    context.server_thread.daemon = True
    context.server_thread.start()
    time.sleep(5)
    
    context.wait_seconds = WAIT_SECONDS
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)
    # context.driver.implicitly_wait(context.wait_seconds)
    
    requests.post(f"{BASE_URL}/pets/reset")
    
    
def after_all(context):
    context.driver.quit()
    requests.get(f"{BASE_URL}/shutdown")