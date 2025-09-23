# Variable Substitutions and Continuing Tests After Failure

In this exercise, we will implement a new BDD scenario for our pet shop project. We will focus on:
- Using Selenium to interact with a web form.
- Getting data from a text field and using it in a test.
- Asserting that multiple form fields are populated with the correct data.

We will use the provided feature file as our starting point. This new scenario will demonstrate how a user can search for a pet by ID and see the results appear in the form.

## Part 1: Implement the web steps

We need to implement the steps that handle searching by ID and checking the values in the form fields. This will require new step definitions that can handle different HTML elements, including text inputs, checkboxes, and select dropdowns. For similar statements, make sure to use variable substitutions to avoid implementing redundant steps.

### Step 1

Implement the step for `Given I am on the "Home Page"`.

```py
@given('I am on the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)
```

### Step 2

Implement the step for `When I set the "Pet ID" to "1"`. Use a variable for the pet ID so that the step can be used for other IDs.

```py
ID_PREFIX = 'pet_'

@when('I set the "Pet ID" to "{pet_id}"')
def step_impl(context, pet_id):
    element = context.driver.find_element(By.ID, ID_PREFIX + 'id')
    element.clear()
    element.send_keys(pet_id)
```

### Step 3

Implement the step for `And I click the "Search" button`. Use a variable for the button name, just in case we would need a similar step for another button.

```py
@when('I click the "{button}" button')
def step_impl(context, button):
    button_id = button.lower() + '-btn'
    context.driver.find_element(By.ID, button_id).click()
```

### Step 4

Implement the step for `Then I should see the message "Success"`. Use a variable for the message string. Use `WebDriverWait` so that the element is properly rendered before being accessed.

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
```

### Step 5

Implement the step for `And the "..." field should contain "..."`. Use variables for the field name and the contents. For this step, the text field elements are static elements, therefore there is no need for using `WebDriverWait`.

```py
@then('the "{field_name}" field should contain "{text_string}"')
def step_impl(context, field_name, text_string):
    element_id = ID_PREFIX + field_name.lower()
    element = context.driver.find_element(By.ID, element_id)
    assert(text_string == element.get_attribute('value'))
```

### Step 6

Implement the step for `And the "..." checkbox should be checked`. Use a variable for the checkbox name.

```py
@then('the "{field_name}" checkbox should be {state}')
def step_impl(context, field_name, state):
    element_id = ID_PREFIX + field_name.lower()
    element = context.driver.find_element(By.ID, element_id)
    if state == 'checked':
        assert(element.is_selected())
    else:
        assert(not element.is_selected())
```

### Step 7

Implement the step for `And the "..." select should contain "..."`. Use a variable for the selector name and the value.

```py
from selenium.webdriver.support.ui import Select

@then('the "{field_name}" select should contain "{text_string}"')
def step_impl(context, field_name, text_string):
    element_id = ID_PREFIX + field_name.lower()
    select = Select(context.driver.find_element(By.ID, element_id))
    assert(text_string == select.first_selected_option.text)
```

## Part 2: Make the test continue after failure

Run the `behave` tests and observe the results. You should see the following output in your terminal.

```
    Given I am on the "Home Page"                         # features/steps/web_steps.py:26
    When I set the "Pet ID" to "1"                        # features/steps/web_steps.py:31 0.093s
    And I click the "Search" button                       # features/steps/web_steps.py:38 0.067s
    And the "Name" field should contain "Fido"            # features/steps/web_steps.py:54 0.015s
      ASSERT FAILED:ield should contain "Fido"            # features/steps/web_steps.py:54

    And the "Category" field should contain "dog"         # None
    And the "Available" checkbox should be checked        # None
    And the "Gender" select should contain "MALE"         # None
    And the "Birthday" field should contain "2019-11-18"  # None
```

From the results above, we can see that some steps passed, one step failed, and the rest were skipped. The failure is expected because the search-by-ID feature is not yet implemented in the application. However, this is a perfect example of a situation where we want the scenario to continue even after a failure has occurred.

### Step 1

Add the `@continue_after_failed_step` tag to your feature file, just before the `Scenario` keyword.

```gherkin
@continue_after_failed_step
Scenario: Search for a pet by ID and populate the form
    Given I am on the "Home Page"
    When I set the "Pet ID" to "1"
    And I click the "Search" button
    ...
```

### Step 2

In your `environment.py file`, add a `before_scenario` hook that checks for the tag and enables the "continue after failed step" behavior. This is how you tell Behave to honor the tag.

```py
def before_scenario(context, scenario):
    if "continue_after_failed_step" in scenario.effective_tags:
        scenario.continue_after_failed_step = True
```

Now, try running behave one more time and observe the results. You should see that the test now runs to the end, regardless of a step failure in the middle of the scenario.
