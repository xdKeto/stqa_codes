BASE_URL = 'http://localhost:5000'

def before_all(context):
    """
    Executes once before all tests.
    Sets the base URL.
    """
    context.base_url = BASE_URL

def after_all(context):
    """
    Executes once after all tests.
    This hook is intentionally empty to demonstrate a simple setup.
    """
    pass
