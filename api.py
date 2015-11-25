import logging
import status
import trafaret as t

from graphql.core.error import GraphQLError
from flask import request, redirect
from flask.ext.api import FlaskAPI
from flask.ext.api.decorators import set_parsers
from flask_debugtoolbar import DebugToolbarExtension
from flask_swagger import swagger
from ql import schema

from factories import *
from models import *
from utils import *

app = FlaskAPI(__name__, static_url_path='/static')
app.config.from_object('settings.DevConfig')

toolbar = DebugToolbarExtension(app)

logger = logging.getLogger('app')


def user_query(email):
    return '''
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


@app.route('/ui')
def ui():
    return redirect('/static/index.html')


@app.route('/ql', methods=['GET', 'POST'])
@set_parsers(GraphQLParser)
def index():
    """
    GraphQL query

    query Yo {
      user(email: "$email" ) {
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
    result_hash = format_result(result)
    return result_hash


@app.route('/graph-query', methods=['GET', 'POST'])
def query():
    """
    GraphQL query

    # query Yo {
    #   user(email: "$email" ) {
    #         email,
    #         posts {
    #             title
    #             etags
    #             tags
    #             comments {
    #                 name
    #                 content
    #             }
    #         }
    #   }
    # }

    """
    query = request.json.get('query')
    logger.debug('Query: %s', request.json)
    result = schema.execute(query)
    result_hash = format_result(result)
    return result_hash


@app.route('/ql/<user_id>/posts', methods=['POST'])
def create_post(user_id):
    post_schema = t.Dict({
        'title': t.String(min_length=2),
        'content': t.String(min_length=2),
        t.Key('tags',
              optional=True): t.List(t.String,
                                     min_length=1),
    })

    post_data = post_schema.check(request.data)
    user = User.objects.get_or_404(id=user_id)
    post = Post(author=user, **post_data)
    post.save()
    logger.debug('New post id %s', post.id)
    # publish data to user channel
    return {'id': str(post.id)}, status.HTTP_201_CREATED


@app.route('/ql/users', methods=['POST'])
def create_user():
    user_schema = t.Dict({
        'email': t.String(min_length=2),
        'first_name': t.String(min_length=2),
        'last_name': t.String(min_length=2),
    })

    user_data = user_schema.check(request.data)
    user = User.objects.create(**user_data)
    user.save()
    return {'id': str(user.id)}, status.HTTP_201_CREATED


@app.route('/ql/<user_id>/posts/<post_id>', methods=['POST'])
def create_comment(user_id, post_id):
    comment_schema = t.Dict({'name': t.String(min_length=2, max_length=30), 'content': t.String(min_length=2),})

    comment_data = comment_schema.check(request.data)
    post = Post.objects.get_or_404(id=post_id)
    logger.debug(comment_data)
    comment = Comment(**comment_data)
    post.comments.append(comment)
    post.save()
    # publish data to user channel
    return {'id': str(comment.id)}, status.HTTP_201_CREATED


@app.errorhandler(t.DataError)
def handle_invalid_usage(data_error):
    error_details = {k: str(v) for k, v in data_error.error.items()}
    logger.error('Validation errors: %s', error_details)
    return error_details, status.HTTP_400_BAD_REQUEST


@app.errorhandler(GraphQLError)
def handle_invalid_usage(graphql_error):
    logger.exception(graphql_error)
    return {}, status.HTTP_400_BAD_REQUEST


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
