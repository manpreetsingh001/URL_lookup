#!/usr/bin/python
import sys
sys.path.append("..")

from mock import patch
from URL_lookup import app
from URL_lookup import search
import unittest,json
from mock import MagicMock

class TestSearch(unittest.TestCase):
  '''Unit test for URL lookuo service'''

  @classmethod
  def setUpClass(cls):
    pass

  @classmethod
  def tearDownClass(cls):
    pass

  def setUp(self):
    # creates a test client
    self.app = app.test_client()
    # create a app and request context
    self.app_context = app.app_context()
    self.app_ctx     = app.test_request_context()

    self.app_context.push()
    self.app_ctx.push()

  def tearDown(self):
    self.app_context.pop()
    self.app_ctx.pop()

    # propagate the exceptions to the test client
    self.app.testing = True

  def test_search_non_malicious_url(self,new_URL='google.com'):
    # sends HTTP GET request to the application
      # on the specified path

    with patch ('mysql.connector.connect') as mock_db:
    #patching a mysql connector so that for testing it doesn't connect to database
      connection = mock_db.return_value
      cursor = connection.cursor.return_value

      cursor.fetchone.return_value = (0,)

      data = dict(Current_status = "Safe Browsing", Recent_activity = "No  malicious content seen Redirecting you on .... {}".format(new_URL)) #expected value
      expected = json.dumps(data)

      result = self.app.get('/urlinfo/1/http://{}'.format(new_URL))

      self.assertEqual(result.data , expected )
      cursor.execute.assert_called_once_with("SELECT COUNT(1) FROM URLlookup where malicious = '{}' ".format(new_URL))

  def test_search_malicious_url(self,new_URL="sunlux.net/company/about.html"):
    #send HTTP get request to the application
    #on the specified path

    with patch ('mysql.connector.connect') as mock_db:
    #patching a mysql connector so that for testing it doesn't connect to database
      connection = mock_db.return_value
      cursor = connection.cursor.return_value

      cursor.fetchone.return_value = (1,)

      data = dict(Current_status = "Dangerous Site",Recent_activity = "Malicious content seen on {}".format(new_URL))  #expected value
      expected = json.dumps(data)

      result = self.app.get('/urlinfo/1/http://www.{0}'.format(new_URL))
      self.assertEqual( result.data , expected)
      cursor.execute.assert_called_once_with("SELECT COUNT(1) FROM URLlookup where malicious = '{}' ".format(new_URL))

  def test_search_invalid_url(self,new_URL="google"):
    #send Invalid URL  and it should warn 
     data = dict(Invalid_URL_Format="Please Enter a valid URL format like http://www.example.com")
     expected = json.dumps(data)

     result = self.app.get('/urlinfo/1/http://{0}'.format(new_URL))
     self.assertEqual( result.data , expected)

  def test_search_url_with_path(self,new_URL='google.com/images'):
   #send URL with path
    with patch ('mysql.connector.connect') as mock_db:
    #patching a mysql connector so that for testing it
      connection = mock_db.return_value
      cursor = connection.cursor.return_value

      cursor.fetchone.return_value = (0,)

      data = dict(Current_status = "Safe Browsing", Recent_activity = "No  malicious content seen Redirecting you on .... {}".format(new_URL)) #expected value
      expected = json.dumps(data)

      result = self.app.get('/urlinfo/1/http://{}'.format(new_URL))

      self.assertEqual(result.data , expected )
      cursor.execute.assert_called_once_with("SELECT COUNT(1) FROM URLlookup where malicious = '{}' ".format(new_URL))


if __name__ == '__main__':
    unittest.main()


