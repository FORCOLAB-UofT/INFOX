import unittest

from flask import current_app
from app import create_app


class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_exists(self):
        """ Check start of app successfully.
        """
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """ Check app using TestConfig.
        """
        self.assertTrue(current_app.config['TESTING'])
