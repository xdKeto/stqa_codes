## BDD with Behave: Hit Counter

This project is a simple demonstration of Behavior-Driven Development (BDD) using the behave framework and a minimal Flask application. The goal is to verify that a simple hit counter works as expected.

For starters, you should study the simple app. You can even run it and open the app in a web browser to find out how it looks like.

### Step 1: Create the Feature File

The first step in BDD is to describe the application's behavior in a human-readable format. We will create a feature file that describes a user clicking a button and seeing a counter increment. Create a new file named `counter.feature` inside the `features` folder.

For the first part, we should create a feature called "Hit Counter". Write down the feature from the perspective of a website visitor. The visitor should be able to click a button so that the counter on the web adds up. Use the following user story format:
```
Feature: <Title>

As a <role>
I want <functionality>
So that <benefit>
```

Now create a scenario that simulates the behavior of the website when the button is clicked. The scenario should show that when the button is clicked, the counter goes up. Make sure to test button clicks more than 1 time. Use the following Gherkin syntax.
```
Scenario: <scenario name>
    Given ...
    When ...
    Then ...
```

### Solution for Step 1
```
Feature: Hit Counter
    As a website visitor
    I want to be able to click a button to make the counter go up
    So that I can see how many times I have clicked the button

Scenario: The counter goes up when the button is clicked
    Given the counter is reset
    When a user clicks the "Hit" button
    Then the counter should be at 1
    When a user clicks the "Hit" button
    Then the counter should be at 2
```

## Step 2: Write the Step Definitions

Next, we need to implement the Python code that will execute the steps in our feature file. This will be done by making direct API calls to the Flask application, simulating the behavior described in the feature file.

Create a new file named `web_steps.py` inside the `features/steps` folder.

#### First Step: The Imports

Start by adding the necessary imports and the base URL for our Flask app. We will need the requests library to make HTTP calls.

```py
from behave import given, when, then
import requests
```

#### Second Step: Implement the Given statement

The `Given the counter is reset` step needs to make an API call to reset the counter on the Flask app. Write a function that uses the `requests` library and the `BASE_URL`. Use the following decorator and function format.

```py
@given('<precondition>')
def step_impl(context):
    # Send a post request to the appropriate route to reset
    # Assert the status code is 200
```

#### Third Step: Implement the When statement

The `When a user clicks the "Hit" button` step needs to simulate a button click by calling the `/hit` API endpoint. Write a function to handle this.

```py
@when('<event happens>')
def step_impl(context):
    # Send a post request to the appropriate route to hit
    # Assert the status code is 200
```

#### Fourth Step: Implement the Then statement

The `Then the counter should be at {count}` step needs to verify that the counter on the web page has the expected value. The `{count}` in the step definition is a variable that will be passed into our Python function. To make the assertion easier, we can simply assume `"<span id=\"counter\">{count}</span>"` is found inside `response.text`.

```py
@then('<outcome observed with {count}>')
def step_impl(context):
    # Send a get request to acquire the returned web page
    # Assert the counter has the expected value
```

### Solution for Step 2
```py
from behave import given, when, then
import requests

@given('the counter is reset')
def step_impl(context):
    """Resets the hit counter via an API call."""
    response = requests.post(f"{context.base_url}/reset")
    assert response.status_code == 200

@when('a user clicks the "Hit" button')
def step_impl(context):
    """Simulates a button click with an API call."""
    response = requests.post(f"{context.base_url}/hit")
    assert response.status_code == 200

@then('the counter should be at {count}')
def step_impl(context, count):
    """Verifies that the counter has the expected value."""
    response = requests.get(f"{context.base_url}/")
    assert f"<span id=\"counter\">{count}</span>" in response.text
```

## Step 3: Run the Tests

To run the BDD tests, we must first start the Flask application manually in one terminal.

```
python app.py
```

In a second terminal, navigate to the project's root directory and run the `behave` command to execute our tests.

```
behave
```

The result should look like this:

```
Feature: Hit Counter # features/counter.feature:1
  As a website visitor
  I want to be able to click a button
  So that a counter adds up
  Scenario: A user clicks the button    # features/counter.feature:7
    Given the counter is reset          # features/steps/web_steps.py:4
    When a user clicks the "Hit" button # features/steps/web_steps.py:10
    Then the counter should be at 1     # features/steps/web_steps.py:15
    When a user clicks the "Hit" button # features/steps/web_steps.py:10
    Then the counter should be at 2     # features/steps/web_steps.py:15

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
5 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m10.167s
```
