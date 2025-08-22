Commands for running tests:
- pytest -v --cov=models
- pytest -v --cov=models --cov-report=term-missing

To do list:
1. Create class-level fixtures:  
   a. In the setUpClass method:
      - Open connection to database using SQL Alchemy command:
      ```py
      db.create_all()
      ```
      - Load test data from a provided json file into memory using the command:
      ```py
      global ACCOUNT_DATA
      with open('tests/fixtures/account_data.json') as json_data:
          ACCOUNT_DATA = json.load(json_data)
      ```
   b. In the tearDownClass method:
      - Disconnect from database using the command:
      ```py
      db.session.remove()
      ```
    
3. Run an initial test
   ```bash
   pytest -v --cov=models --cov-report=term-missing
   ```
   You should see that many parts of the code for account.py are not covered by test cases, since there are no test cases yet.

4. Create a test case for creating an account, and run the test
   ```py
   def test_create_account(self):
       """ Test create an account """
       account = Account(**ACCOUNT_DATA[0])
       account.create()
       self.assertEqual(len(Account.all()), 1)
   ```
   ```bash
   pytest -v --cov=models --cov-report=term-missing
   ```
   Try running the tests once more. You should see that the test fails on the second run.
   
5. Create test-level fixtures:  
   a. In the setUp method:
      - Truncate the tables
      ```py
      db.session.query(Account).delete()
      ```
   b. Rerun the tests:
   ```bash
   pytest -v --cov=models --cov-report=term-missing
   ```
   
6. Create a test case for creating all accounts in the json file, and rerun the test
   ```py
   def test_create_all_accounts(self):
       """ Test create all accounts """
       for data in ACCOUNT_DATA:
           account = Account(**data)
           account.create()
       self.assertEqual(len(Account.all()), len(ACCOUNT_DATA))
   ```
   ```bash
   pytest -v --cov=models --cov-report=term-missing
   ```
   Try running the tests once more.

7. Continue implementing tests to raise the coverage further.
