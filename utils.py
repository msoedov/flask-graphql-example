import logging
from flask_api import parsers
from graphql.core.error import GraphQLError, format_error

from factories import *
from models import *


logger = logging.getLogger(__package__)


class GraphQLParser(parsers.BaseParser):

    """docstring for GraphQLParser"""

    # media_type = 'application/graphql'
    media_type = '*/*'

    def parse(self, stream, media_type, content_length=None):
        data = stream.read().decode('ascii')
        return data


def form_error(error):
    if isinstance(error, GraphQLError):
        return format_error(error)
    return error


def format_result(result):
    if result.errors:
        logger.debug(result.errors)
        raise result.errors[0]
    data = result.data
    return data


def run_query(schema, query):
    result = schema.execute(query)
    result_hash = format_result(result)
    return result_hash
