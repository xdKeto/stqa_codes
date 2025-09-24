# BDD with Behave and Selenium: Pet Shop

This project is a demonstration of Behavior-Driven Development (BDD) using the `behave` framework and `selenium` to test a web application. The goal is to verify that a user can interact with a pet shop website to search for pets by category. To get a good idea of what the application does, you should:
- Study the provided codes and feature file.
- Run the application on localhost and try out the user interface.

## Step 1: Create the Behave Environment

The `environment.py` file is responsible for setting up and tearing down the test environment. In this step, you will implement the `behave` hooks to start the Flask application and initialize the Selenium WebDriver.

### Part 1.1: Base URL and Hooks

Open the empty `environment.py` file. Define the `BASE_URL` and a basic `before_all` hook. The URL is where your Flask app will be running.

```py
from os import getenv

BASE_URL = getenv('BASE_URL', 'http://localhost:5000')

def before_all(context):
    """ Executed once before all tests """
    context.base_url = BASE_URL
```

### Part 1.2: Launch the Flask App

Now, add the code to start your Flask app in a separate thread. This ensures the app is running in the background when your tests begin.

Steps:
- Import the `threading` and `time` modules.
- Import the `app` instance from your `app.py`.
- Create a new `threading.Thread` and set it as a daemon.
- Add a small delay to give the server time to start up.

```py
import threading
import time
from app import app as flask_app

def before_all(context):
    # Start the Flask app in a separate thread
    context.server_thread = threading.Thread(
        target=flask_app.run,
        kwargs={'host': '0.0.0.0', 'port': 5000}
    )
    context.server_thread.daemon = True
    context.server_thread.start()
    time.sleep(5)
```

### Part 1.3: Initialize the WebDriver

Add the code to initialize the Selenium Chrome WebDriver. You should configure it to run in headless mode for efficiency.

Steps:
- Import the `webdriver` from `selenium`.
- Use `webdriver.ChromeOptions()` to set up the headless and no-sandbox arguments.
- Set the `context.driver` and a default `implicitly_wait` time.

```py
from selenium import webdriver

WAIT_SECONDS = int(getenv('WAIT_SECONDS', '60'))

def before_all(context):
    context.wait_seconds = WAIT_SECONDS

    # Instantiate the Chrome WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    context.driver = webdriver.Chrome(options=options)
```

### Part 1.4: The Remaining Hooks

Complete the `environment.py` file with the remaining hooks. These will ensure the app and database are in a clean state before each test run and that all resources are shut down afterward.

Steps:
- Add a `requests` import to send API calls for cleanup.
- The `before_all` hook should make a `POST` request to `/pets/reset` to clear the database.
- The `after_all` hook should gracefully quit the `WebDriver` and shut down the server.

```py
import requests

def before_all(context):
    # This step is crucial to ensure a clean database
    requests.post(f"{BASE_URL}/pets/reset")

def after_all(context):
    """ Executed after all tests """
    # Gracefully shut down the webdriver
    context.driver.quit()
    
    # We need to send a shutdown request to the server
    # to stop the server thread cleanly
    requests.get(f"{BASE_URL}/shutdown")
```

## Step 2: Implement the Step Definitions

Next, you will create a new file named `web_steps.py` inside the `features/steps` folder. This file will contain all the Python functions that interact with the web page using Selenium.

### Part 2.1: Loading the Test Data

The `Given` step loads the initial data from the feature file's `Background` table into the database. This requires a `requests` import and an assertion to confirm the data was loaded.

Steps:
- Import the `given` decorator from `behave` and the `requests` library.
- Clean up the database first
- Iterate through `context.table` to get each row of data.
- Send a `POST` request to the `/pets` endpoint for each pet.

```py
import requests
from behave import given

@given('the following pets')
def step_impl(context):
    """Refresh pets in database"""
    # This ensures a clean database before loading the data table
    requests.post(f"{context.base_url}/pets/reset")
    
    for row in context.table:
        result = {
            "name": row['name'],
            "category": row['category'],
            "available": row['available'] in ['True', 'true', '1'],
            "gender": row['gender'],
            "birthday": row['birthday']
        }
        response = requests.post(f"{context.base_url}/pets", json=result)
        assert(response.status_code == 201)
```

### Part 2.2: The Web Interaction Steps

Now, implement the steps that use Selenium to interact with the web page.

Steps:
- Import `By`, `WebDriverWait`, and `expected_conditions` from the `selenium` library.
- Use `context.driver.get()` to navigate to the base URL.
- Use `context.driver.find_element(By.ID, ...)` to locate elements.
- The element ID for "Category" should be `pet_category`, and the button ID should be `search-btn`.

```py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

ID_PREFIX = 'pet_'

@given('I am on the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)

@when('I set the "{element_name}" to "{text_string}"')
def step_impl(context, element_name, text_string):
    element_id = ID_PREFIX + element_name.lower().replace(' ', '_')
    element = context.driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(text_string)

@when('I click the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()
```

### Part 2.3: The Assertions

Finally, implement the `then` steps that assert the state of the web page. This is where you will check for messages and the presence of pet names in the search results.

Steps:
- Use `WebDriverWait` with `expected_conditions` to wait for elements and text to be present. This is crucial for handling dynamic page content.
- The `flash_message` and `search_results` divs should have the correct IDs.
- Make your assertions.

```py
@then('I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'flash_message'),
            message
        )
    )
    assert(found)

@then('I should see "{name}" in the results')
def step_impl(context, name):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, 'search_results'),
            name
        )
    )
    assert(found)

@then('I should not see "{name}" in the results')
def step_impl(context, name):
    element = context.driver.find_element(By.ID, 'search_results')
    assert(name not in element.text)
```

## Step 3: Run the Tests

Run the behave command to execute your tests.

```
behave
```
