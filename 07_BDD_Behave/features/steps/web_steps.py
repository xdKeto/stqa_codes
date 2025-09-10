from behave import given, when, then
import requests

@given('the counter is reset')
def reset_impl(context):
    response = requests.post(context.base_url + "/reset")
    assert(response.status_code, 200)
    
@when('the "Hit" button is clicked')
def hit_impl(context):
    response = requests.post(context.base_url + "/hit")
    assert(response.status_code, 200)
    
@then('the counter shows value {count}')
def counter_impl(context, count):
    response = requests.get(context.base_url)
    assert('<span id=\"counter\">{count}</span>' in response.text)
    