import unittest

from flask import current_app
from app import create_app
from flask.testing import FlaskClient



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

    def test_followed_endpoint_without_auth(self):
        tester = self.app.test_client()
        response = tester.get("/flask/followed", headers={"Authorization": "Basic "})

        self.assertTrue(response.status_code == 401)
       # assert response.status_code == 200

    def test_import_endpoint_without_auth(self):
        tester = self.app.test_client()
        response = tester.get("/flask/import", headers={"Authorization": "Basic "})

        self.assertTrue(response.status_code == 401)

    def test_auth_endpoint_without_auth(self):
        tester = self.app.test_client()
        response = tester.get("/flask/auth", headers={"Authorization": "Basic "})

        self.assertTrue(response.status_code == 401)
    
    def test_search_endpoint(self):
        tester = self.app.test_client()
        response = tester.get("/flask/search", headers={"Authorization": "Basic "})

        assert response.status_code == 405

    def test_follow_endpoint_without_auth(self):
        tester = self.app.test_client()
        response = tester.get("/flask/follow", headers={"Authorization": "Basic "})

        self.assertTrue(response.status_code == 405)

    def test_cluster_endpoint_without_auth(self):
        tester = self.app.test_client()
        response = tester.get("/flask/cluster?repo=freeCodeCamp/freeCodeCamp&analyzeCode=true&analyzeFiles=true&analyzeCommits=true&clusterNumber=10&userInputWords=challenges,curriculum,responsive,org,readme", headers={"Authorization": "Basic "})

        self.assertTrue(response.status_code == 401)

