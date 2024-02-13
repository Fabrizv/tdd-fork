"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
import json
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""
    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
    def setUp(self):
        self.client = app.test_client()
    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        result = self.client.post('/counters/uc')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        base_result = self.client.get('/counters/uc')
        base_value = json.loads(base_result.data)["uc"]

        update_result = self.client.put('/counters/uc')
        self.assertEqual(update_result.status_code, status.HTTP_200_OK)

        new_result = self.client.get('/counters/uc')
        new_value = json.loads(new_result.data)["uc"]
        self.assertEqual(new_value, base_value + 1)

        no_result = self.client.put('/counters/no_uc')
        self.assertEqual(no_result.status_code, status.HTTP_404_NOT_FOUND)
        response_data = json.loads(no_result.data)
        self.assertEqual(response_data["error"], "Counter not found")


    def test_read_counter(self):
        """It should read a counter"""
        client = app.test_client()
        result = client.post('/counters/rc')
        result = client.get('/counters/rc')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        result2 = client.get('/counters/doesnotexist')
        self.assertEqual(result2.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_counter(self):
        """It should error for deleting"""
        client = app.test_client()
        client.post('/counters/dc')
        client.put('/counters/dc')
        getResult = client.delete('/counters/dc')
        self.assertEqual(getResult.status_code, status.HTTP_204_NO_CONTENT)
        getResult = client.delete('/counters/dc2')
        self.assertEqual(getResult.status_code, status.HTTP_404_NOT_FOUND)
