Commands for running tests:
- pytest -v --cov=models
- pytest -v --cov=models --cov-report=term-missing

To do list:
1. In the setUpClass method:
  - Open connection to database using SQL Alchemy command: db.create_all()
  - Declare ACCOUNT_DATA as a global variable with the command: global ACCOUNT_DATA
  - Load test data using the command:
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

2. In the tearDownClass method:
  - Disconnect from database using the command: db.session.close()
