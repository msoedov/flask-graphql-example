import logging

import status
import trafaret as t
from flask import redirect, request
from flask.ext.api import FlaskAPI
from flask_debugtoolbar import DebugToolbarExtension
from flask_swagger import swagger
from graphql.core.error import GraphQLError, format_error

from factories import *
from models import *
from ql import schema
from utils import *

app = FlaskAPI(__name__, static_url_path='/static')
app.config.from_object('settings.DevConfig')

toolbar = DebugToolbarExtension(app)

logger = logging.getLogger(__package__)


@app.route('/ui')
def ui():
    return redirect('/static/index.html')


@app.route('/graph-query', methods=['POST'])
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
    variables = request.json.get('variables') # Todo: add handling variables
    logger.debug('Query: %s', request.json)
    result = schema.execute(query)
    result_hash = format_result(result)
    return result_hash


@app.errorhandler(t.DataError)
def handle_invalid_usage(data_error):
    error_details = {k: str(v) for k, v in data_error.error.items()}
    logger.error('Validation errors: %s', error_details)
    return error_details, status.HTTP_400_BAD_REQUEST


@app.errorhandler(GraphQLError)
def handle_invalid_graph_error(graphql_error):
    error_message = format_error(graphql_error)
    logger.error(error_message)
    return {'error': error_message}, status.HTTP_400_BAD_REQUEST


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
