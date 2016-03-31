''' Exports UserService. '''

from datetime import datetime
from szurubooru.model.user import User

class UserService(object):
    ''' User management '''

    def __init__(self, config, password_service):
        self._config = config
        self._password_service = password_service

    def create_user(self, session, name, password, email):
        ''' Creates an user with given parameters and returns it. '''
        user = User()
        user.name = name
        user.password = password
        user.password_salt = self._password_service.create_password()
        user.password_hash = self._password_service.get_password_hash(
            user.password_salt, user.password)
        user.email = email
        user.access_rank = self._config['service']['default_user_rank']
        user.creation_time = datetime.now()
        user.avatar_style = User.AVATAR_GRAVATAR

        session.add(user)
        return user

    def get_by_name(self, session, name):
        ''' Retrieves an user by its name. '''
        return session.query(User).filter_by(name=name).first()