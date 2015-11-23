from flask.ext.testing import TestCase
from flask import url_for
from factories import UserFactory
from api import app


class AppTestCase(TestCase):

    def create_app(self):
        return app

    def test_post_creation(self):
        author = UserFactory()
        response = self.client.post(url_for('create_post', user_id=author.id),
                                    data={'title': 'Test title', 'content': 'test-content'})
        self.assertEqual(response.status_code, 201)
        # Check that the response body is empty
        self.assertEqual(response.json, {})

    def test_post_validation(self):

        bad_posts = [{}, {'foo': 2}, {'tags': []}]

        author = UserFactory()

        for p in bad_posts:
            response = self.client.post(url_for('create_post', user_id=author.id),
                                        data=p)
            self.assertEqual(response.status_code, 400)
