## Create a counter

You will start by implementing a test case to test creating a counter. Following REST API guidelines, a create uses a `POST` request and returns code `201_CREATED` if successful. You can call the routes of the app client using the syntax `client.<METHOD>("<ROUTE>")`, for example `client.post("/counters/<name>")`.

Then you’ll write the code to make the test pass. Use the route `/counters/<name>` with the method `POST`. You can store the counter data in a global variable. Create a function that creates a counter with the specified name. You can use a tuple (response, status_code) as the return format of the route function. The response can simply be a python dictionary.

### Solution for Create a counter
```py
@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Creates a counter"""
    global COUNTERS
    COUNTERS[name] = 1
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED
```
```py
def test_create_counter(self):
    result = self.client.post("/counters/test-counter")
    self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    data = result.get_json()
    self.assertIn("test-counter", data)
    self.assertEqual(data["test-counter"], 1)
```

## Error in creating a duplicate counter

You will implement a test case to test creating a counter with a name that already exists. First, call the route to create a counter with a certain name (you can choose the name yourself). Make sure the method returns code `201_CREATED`.

Next, you should call the same route with the exact same name. Make sure now the method returns `409_CONFLICT`.

If you have not implemented the check to make sure the counter to be created does not already exist, now is the time to add it to the method. If the specified counter name already exists, it should return the code `409_CONFLICT`.

## Update a counter

You will implement a test case to test updating a counter. Following REST API guidelines, an update uses a `PUT` request and returns code `200_OK` if successful. Create a counter and then update it.

Then you’ll write the code to make the test pass. If you’re unfamiliar with Flask, note that all of the routes for the counter service are the same; only the method changes.

Next, you will implement a function to update the counter. Per REST API guidelines, an update uses a PUT request and returns a `200_OK` code if successful. Create a function that updates the counter that matches the specified name.

## Read a counter

Next, you will write a test case to read a counter. Following REST API guidelines, a read uses a `GET` request and returns a `200_OK` code if successful. Create a counter and then read it.

Once again, it's time to write code to make a test pass. You will implement the code for read a counter. Per REST API guidelines, a read uses a GET request and returns a `200_OK` code if successful. Create a function that returns the counter that matches the specified name.

## Delete a counter

Now you will write a test case to delete a counter. Per REST API guidelines, a read uses a `DELETE` request and returns a `204_NO_CONTENT` code if successful. Create a function that deletes the counter that matches the specified name.

In this last step, you will again write code to make a test pass. This time, you will implement the code to delete a counter. Per REST API guidelines, a delete uses a `DELETE` request and returns a `204_NO_CONTENT` code if successful.
