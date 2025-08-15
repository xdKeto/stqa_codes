from unittest import TestCase
from stack import Stack

class TestStack(TestCase):
    """Test cases for Stack"""

    def setUp(self):
        """Setup before each test"""
        self.stack = Stack()

    def tearDown(self):
        """Tear down after each test"""
        self.stack = None

    def test_push_peek(self):
        """Test pushing an item into the stack and peeking into the stack"""
        # Push 3 into the stack
        # Assert equal: peek result equal to 3
        # Push 5 into the stack
        # Assert equal: peek result equal to 5
        raise Exception("not implemented")

    def test_pop(self):
        """Test popping an item of off the stack"""
        # Push 3 into the stack
        # Push 5 into the stack
        # Assert equal: pop result equal to 5
        # Assert equal: peek result equal to 3
        # Pop from the stack
        # Assert true: stack is empty
        raise Exception("not implemented")

    def test_is_empty(self):
        """Test if the stack is empty"""
        # Assert true: the stack is empty
        # Push 5 into the stack
        # Assert false: the stack is empty
        raise Exception("not implemented")
