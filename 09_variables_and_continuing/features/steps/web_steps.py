from selenium.webdriver.support.ui import Select
import requests
from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

@given('the following pets')
def step_impl(context):
    """ Reset database and load data from feature file """
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

@given(u'I am on the "Home Page"')
def step_impl(context):
    context.driver.get(context.base_url)
    

ID_PREFIX = "pet_"
BUTTON_SUFFIX = '-btn'

@when(u'I set the "Pet ID" to "{pet_id}"')
def step_impl(context, pet_id):
    element = context.driver.find_element(By.ID, ID_PREFIX + "pet_id")
    element.clear()
    element.send_keys(pet_id)


@when(u'I click the "{button_name}" button')
def step_impl(context, button_name):
    button_id = button_name.lower() + BUTTON_SUFFIX
    context.driver.find_element(By.ID, button_id).click()

@then(u'I should see the message "{message}"')
def step_impl(context, message):
    found = WebDriverWait(context.driver, context.wait_seconds).until(
        expected_conditions.text_to_be_present_in_element(
            (By.ID, "flash_message"), 
            message
        )
    )
    assert(found)

@then('the "{field_name}" field should contain "{text_string}"')
def step_impl(context, field_name, text_string):
    element_id = ID_PREFIX + field_name.lower()
    element = context.driver.find_element(By.ID, element_id)
    assert(text_string == element.get_attribute('value'))


@then('the "{field_name}" checkbox should be {state}')
def step_impl(context, field_name, state):
    element_id = ID_PREFIX + field_name.lower()
    element = context.driver.find_element(By.ID, element_id)
    if state == 'checked':
        assert(element.is_selected())
    else:
        assert(not element.is_selected())
        from selenium.webdriver.support.ui import Select

@then('the "{field_name}" select should contain "{text_string}"')
def step_impl(context, field_name, text_string):
    element_id = ID_PREFIX + field_name.lower()
    select = Select(context.driver.find_element(By.ID, element_id))
    assert(text_string == select.first_selected_option.text)