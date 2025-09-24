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
    context.wait_seconds = WAIT_SECONDS

    # Start the Flask app in a separate thread
    context.server_thread = threading.Thread(
        target=flask_app.run,
        kwargs={'host': '0.0.0.0', 'port': 5000}
    )
    context.server_thread.daemon = True
    context.server_thread.start()
    time.sleep(5)

    # Instantiate the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)

    # This step is crucial to ensure a clean database
    requests.post(f"{BASE_URL}/pets/reset")

def after_all(context):
    """ Executed after all tests """
    # Gracefully shut down the webdriver
    context.driver.quit()
    
    # We need to send a shutdown request to the server
    # to stop the server thread cleanly
    requests.get(f"{BASE_URL}/shutdown")
