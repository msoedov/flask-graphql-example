from flask import url_for
from flask.ext.testing import TestCase

from api import app, schema
from factories import PostFactory, UserFactory
from models import Post
from utils import run_query


class AppTestCase(TestCase):

    def create_app(self):
        return app

    def test_post_creation(self):
        author = UserFactory()
        response = self.client.post(
            url_for('create_post',
                    user_id=author.id),
            data={'title': 'Test title',
                  'content': 'test-content'})
        self.assertEqual(response.status_code, 201)
        # Check that the response body is empty
        self.assertIn('id', response.json)

    def test_post_validation(self):

        bad_posts = [{}, {'foo': 2}, {'tags': []}]

        author = UserFactory()

        for p in bad_posts:
            response = self.client.post(
                url_for('create_post', user_id=author.id), data=p)
            self.assert400(response)

    def test_user_creation(self):
        response = self.client.post(url_for('create_user'), data={
                                    'email': 'foo@bar', 'first_name': 'Joe', 'last_name': 'Doe'})
        self.assertEqual(response.status_code, 201)
        # Check that the response body is empty
        self.assertIn('id', response.json)

    def test_comment_creation(self):
        author = UserFactory()
        post = PostFactory(author=author)
        self.assertEqual(len(post.comments), 5)
        response = self.client.post(url_for('create_comment', user_id=author.id, post_id=post.id), data={
                                    'name': 'foo', 'content': 'bar'})
        self.assertEqual(response.status_code, 201)
        # Check that the response body is empty
        self.assertEqual(response.json, {})
        self.assertEqual(len(Post.objects.get(id=post.id).comments), 6)


class AssertionMixin(object):

    """Deprecated from python 3.2"""

    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        """Checks whether dictionary is a superset of subset."""
        missing = []
        mismatched = []
        for key, value in subset.items():
            if key not in dictionary:
                missing.append(key)
            elif value != dictionary[key]:
                mismatched.append('%s, expected: %s, actual: %s' %
                                  (safe_repr(key), safe_repr(value),
                                   safe_repr(dictionary[key])))

        if not (missing or mismatched):
            return

        standardMsg = ''
        if missing:
            standardMsg = 'Missing: %s' % ','.join(safe_repr(m) for m in
                                                   missing)
        if mismatched:
            if standardMsg:
                standardMsg += '; '
            standardMsg += 'Mismatched values: %s' % ','.join(mismatched)

        self.fail(self._formatMessage(msg, standardMsg))


class QueryTestCase(TestCase):

    def create_app(self):
        return app

    def test_user_creation(self):
        query = """
mutation myFirstMutation {
    createUser(email: "email@host.com", firstName: "Joe", lastName: "Doe") {
        user {
            id
        }
    }
}
        """
        data = run_query(schema, query)

        expect = {
            "createUser": {
                "user": {
                    'id': id
                },
            }
        }
        self.assertEqual(dict(data), expect)
