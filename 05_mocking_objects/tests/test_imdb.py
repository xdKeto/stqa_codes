"""
Test Cases for Mocking Lab
"""
import json
from unittest import TestCase

IMDB_DATA = {}

class TestIMDbDatabase(TestCase):
    """Tests Cases for IMDb Database"""

    @classmethod
    def setUpClass(cls):
        """ Load imdb responses needed by tests """
        global IMDB_DATA
        with open('tests/fixtures/imdb_responses.json') as json_data:
            IMDB_DATA = json.load(json_data)


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################
