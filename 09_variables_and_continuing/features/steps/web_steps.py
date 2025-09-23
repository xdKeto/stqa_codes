import requests
from behave import given, when, then

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
