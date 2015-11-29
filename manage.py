from flask.ext.script import Manager

from api import app, logger
from factories import PostFactory, UserFactory
from models import User

manager = Manager(app)


@manager.command
def init():
    """
    Populate data
    """
    User.objects.filter(email='idella00@hotmail.com').delete()
    user = UserFactory(email='idella00@hotmail.com')
    logger.debug('User %s', user)
    posts = PostFactory.create_batch(10, author=user)
    logger.debug('Created posts %s', posts)


if __name__ == "__main__":
    manager.run()
