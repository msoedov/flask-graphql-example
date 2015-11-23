from app import app

import os
import json
import unittest
from factories import UserFactory
from api import app


class FlaskTestCase(unittest.TestCase):
    # Our first unit test - We are using the unittest
    # library, calling the _add_numbers route from the app
    # passing a pair of numbers, and checking that the
    # returned value, contained on the JSON response, match
    # the sum of those parameters

    def setUp(self):
        self.tester = app.test_client(self)

    def test_post_creation(self):
        author = UserFactory()
        response = self.tester.post('ql/{}/posts'.format(author.id),
                                    content_type='application/json', data={'title': 'Test title', 'content': 'test_content'})
        self.assertEqual(response.status_code, 201)
        # Check that the result sent is 8: 2+6
        self.assertEqual(json.loads(response.data), {"result": 8})


# if __name__ == '__main__':
#     unittest.main()
