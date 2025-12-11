from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import requests
import time

ID_PREFIX = "task_"

@given('the following tasks exist')
def step_create_initial_tasks(context):
    """Create initial tasks from the Background table"""
    # First, reset the database to ensure clean state
    requests.post(f"{context.base_url}/tasks/reset")
    time.sleep(0.5)
    
    # Create each task from the table
    for row in context.table:
        task_data = {
            'name': row['name'],
            'priority': row['priority'],
            'due_date': row['due_date'],
            'status': row['status']
        }
        response = requests.post(
            f'{context.base_url}/tasks',
            json=task_data,
            headers={'Content-Type': 'application/json'}
        )
        assert response.status_code == 201, f"Failed to create task: {row['name']}"
    
    # Navigate to the dashboard to see the tasks
    context.driver.get(context.base_url)
    
    # Wait for the page to fully load
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, "task-list"))
    )
    time.sleep(1)  # Additional wait for page to stabilize

@when('I fill in task "{field}" field with "{value}"')
def step_fill_task_field(context, field, value):
    """Fill in a task form field with the given value"""
    field_id = ID_PREFIX + field
    
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    element.clear()
    element.send_keys(value)
    time.sleep(0.2)  # Small delay for stability

@when('I fill in task "{field}" with "{value}"')
def step_fill_task_field_short(context, field, value):
    """Alternative step for filling task fields (shorter syntax)"""
    field_id = ID_PREFIX + field
    
    element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    element.clear()
    element.send_keys(value)
    time.sleep(0.2)

@when('I select "{option}" from task "{field}" dropdown')
def step_select_from_dropdown(context, option, field):
    """Select an option from a dropdown field"""
    field_id = ID_PREFIX + field
    
    select_element = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, field_id))
    )
    select = Select(select_element)
    select.select_by_value(option)
    time.sleep(0.2)

@when('I click the "{button_text}" button')
def step_click_button(context, button_text):
    """Click a button by its text or ID"""
    # Try to find button by ID first (for "Add Task" button)
    if button_text == "Add Task":
        button = WebDriverWait(context.driver, context.wait_seconds).until(
            EC.element_to_be_clickable((By.ID, "add-task-btn"))
        )
    else:
        # Fallback: find by button text
        button = WebDriverWait(context.driver, context.wait_seconds).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{button_text}')]"))
        )
    
    button.click()
    
    # Wait for page to reload after adding task
    time.sleep(2)
    
    # Wait for task list to be present again after reload
    WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, "task-list"))
    )

@then('I should see the tasks in the following order')
def step_verify_task_order(context):
    """Verify that tasks appear in the expected order"""
    # Wait for task list to be fully loaded
    task_list = WebDriverWait(context.driver, context.wait_seconds).until(
        EC.presence_of_element_located((By.ID, "task-list"))
    )
    
    # Get all task items (excluding "No tasks defined" message)
    task_items = context.driver.find_elements(By.CSS_SELECTOR, "#task-list .task-item")
    
    # Parse expected task names from the text in the Then step
    # The context.text contains the bulleted list like:
    # - Urgent feature
    # - Clean code
    # - Write docs
    # - Interview user
    expected_tasks = []
    if context.text:
        lines = context.text.strip().split('\n')
        for line in lines:
            # Remove leading dash and whitespace
            task_name = line.strip().lstrip('-').strip()
            if task_name:
                expected_tasks.append(task_name)
    
    # Verify we have the correct number of tasks
    actual_count = len(task_items)
    expected_count = len(expected_tasks)
    
    assert actual_count == expected_count, \
        f"Expected {expected_count} tasks, but found {actual_count} tasks"
    
    # Verify each task is in the correct position
    for index, expected_name in enumerate(expected_tasks):
        # Get the task name from the task item at this position
        task_name_element = task_items[index].find_element(By.CSS_SELECTOR, ".task-name")
        actual_name = task_name_element.text.strip()
        
        # Case-insensitive comparison to handle potential case differences
        assert actual_name.lower() == expected_name.lower(), \
            f"Position {index + 1}: Expected '{expected_name}', but got '{actual_name}'"
    
    print(f"✓ All {len(expected_tasks)} tasks are in the correct order")