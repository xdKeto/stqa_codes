"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
from counter import app

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()
