from flask.ext.testing import TestCase

from api import app, schema, GraphQLError
from factories import PostFactory, UserFactory
from utils import run_query


class AssertionMixin(object):

    """Helpfull assertion methods"""

    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        """
        Checks whether dictionary is a superset of subset.
        Deprecated from python 3.2
        https://bugs.python.org/file32662/issue13248.diff
        """
        subset = dict(subset)
        dictionary = dict(dictionary)
        missing = []
        mismatched = []
        for key, value in subset.items():
            if key not in dictionary:
                missing.append(key)
            elif value is id:
                continue
            elif isinstance(dictionary[key], dict) and isinstance(value, dict):
                self.assertDictContainsSubset(value, dictionary[key])
            elif value != dictionary[key]:
                mismatched.append('%s, expected: %s, actual: %s' %
                                  ((key), (value),
                                   (dictionary[key])))

        if not (missing or mismatched):
            return

        standardMsg = ''
        if missing:
            standardMsg = 'Missing: %s' % ','.join((m) for m in
                                                   missing)
        if mismatched:
            if standardMsg:
                standardMsg += '; '
            standardMsg += 'Mismatched values: %s' % ','.join(mismatched)

        self.fail(self._formatMessage(msg, standardMsg))


class QueryTestCase(AssertionMixin, TestCase):

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
        self.assertDictContainsSubset(expect, data)

    def test_user_creation_validation_error(self):
        query = """
mutation myFirstMutation {
    createUser(email: 178, firstName: "Joe", lastName: "Doe") {
        user {
            id
        }
    }
}
        """
        with self.assertRaises(GraphQLError):
            run_query(schema, query)

    def test_post_creation(self):
        user = UserFactory()
        query = """
mutation myFirstMutation {
    createPost(userId: "%s", title: "Just do it", content: "Yesterday you sad tomorrow") {
        post {
            id
        }
    }
}
        """ % user.id
        data = run_query(schema, query)

        expect = {
            "createPost": {
                "post": {
                    'id': id
                },
            }
        }
        self.assertDictContainsSubset(expect, data)

    def test_make_commnet(self):
        post = PostFactory()
        query = """
mutation myFirstMutation {
    makeComment(postId: "%s", name: "Just do it", content: "Yesterday you sad tomorrow") {
        post {
            id
        }
    }
}
        """ % post.id
        data = run_query(schema, query)

        expect = {
            "makeComment": {
                "post": {
                    'id': id
                },
            }
        }
        self.assertDictContainsSubset(expect, data)
