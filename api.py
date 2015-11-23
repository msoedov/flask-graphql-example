import logging

from flask import request, jsonify
from flask.ext.api import FlaskAPI
from flask_swagger import swagger
from factories import *
from models import *
from ql import schema
from flask_debugtoolbar import DebugToolbarExtension
from graphql.core.error import GraphQLError, format_error
from flask.ext.api.decorators import set_parsers
from flask_api import parsers
from utils import *

app = FlaskAPI(__name__)
app.config.from_object('settings')

toolbar = DebugToolbarExtension(app)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@app.route('/init')
def init():
    User.objects.filter(email='idella00@hotmail.com').delete()
    u = UserFactory(email='idella00@hotmail.com')
    posts = PostFactory.create_batch(10, author=u)
    logger.debug(posts[0].comments)
    return posts


def user_query(email):
    return'''
    query Yo {
      user(email: \"%s\") {
            email,
            posts {
                title
                etags
                tags
                comments {
                    name
                    content
                }
            }
      }
    }
    ''' % email


@app.route('/ql', methods=['GET', 'POST'])
@set_parsers(GraphQLParser)
def index():
    """
    Example query
    -----
    query Yo {
      user(email: $email ) {
            email,
            posts {
                title
                etags
                tags
                comments {
                    name
                    content
                }
            }
      }
    }
    """
    query = request.data or user_query("idella00@hotmail.com")

    logger.debug('Query: %s', query)
    result = schema.execute(query)
    r = format_result(result)
    return r

# @app.errorhandler(InvalidAPIUsage)
# def handle_invalid_usage(error):
# response = jsonify(error.to_dict())
# response.status_code = error.status_code
# return response


@app.route('/health-check')
@app.route('/ping')
def health_check():
    """
    Health check
    """
    return {'reply': 'pong'}


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Demo of graphql API endpoint"
    return swag


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=5000)
