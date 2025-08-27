Add pytest options to configuration file pytest.ini.
Commands for running tests:
- pytest

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

```py
def test_repr(self):
    """Test the representation of an account"""
    account = Account()
    account.name = "Foo"
    self.assertEqual(str(account), "<Account 'Foo'>")
```

```py
from random import randrange
```

```py
def setUp(self):
   self.rand = randrange(0, len(ACCOUNT_DATA))

def test_to_dict(self):
    """ Test account to dict """
    data = ACCOUNT_DATA[self.rand]
    account = Account(**data)
    result = account.to_dict()
    self.assertEqual(account.name, result["name"])
    self.assertEqual(account.email, result["email"])
    self.assertEqual(account.phone_number, result["phone_number"])
    self.assertEqual(account.disabled, result["disabled"])
    self.assertEqual(account.date_joined, result["date_joined"])
```

```py
def test_from_dict(self):
    """ Test account from dict """
    data = ACCOUNT_DATA[self.rand]
    account = Account()
    account.from_dict(data)
    self.assertEqual(account.name, data["name"])
    self.assertEqual(account.email, data["email"])
    self.assertEqual(account.phone_number, data["phone_number"])
    self.assertEqual(account.disabled, data["disabled"])
```

```py
def test_update_an_account(self):
    """ Test Account update using known data """
    data = ACCOUNT_DATA[self.rand]
    account = Account(**data)
    account.create()
    self.assertIsNotNone(account.id)
    account.name = "Rumpelstiltskin"
    account.update()
    found = Account.find(account.id)
    self.assertEqual(found.name, account.name)
```

```py
from models.account import DataValidationError
```
```py
def test_invalid_id_on_update(self):
    """ Test invalid ID update """
    data = ACCOUNT_DATA[self.rand]
    account = Account(**data)
    account.id = None
    self.assertRaises(DataValidationError, account.update)
```

```py
def test_delete_an_account(self):
    """ Test Account update using known data """
    data = ACCOUNT_DATA[self.rand]
    account = Account(**data)
    account.create()
    self.assertEqual(len(Account.all()), 1)
    account.delete()
    self.assertEqual(len(Account.all()), 0)
```
