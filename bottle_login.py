import time

import base64
import hashlib
import hmac
import json
import logging
from bottle import request, response, redirect, abort

__version__ = "0.0.3"
__project__ = "bottle-login"
__author__ = "Kirill Klenov <horneds@gmail.com>"
__license__ = "MIT"


logger = logging.getLogger(__name__)


class BottleSession(dict):

    encoding = 'UTF-8'

    def __init__(self, secret, key='session.id', **params):
        self.secret = secret
        self.key = key
        self.params = params
        self.store = {}

    def save(self, set_cookie):
        if set(self.store.items()) ^ set(self.items()):
            value = dict(self.items())
            value = json.dumps(value, indent=None, separators=(',', ':'))
            value = self.encrypt(value)
            if not isinstance(value, str):
                value = value.encode(self.encoding)
            set_cookie(self.key, value, **self.params)

    def load(self, cookies, **kwargs):
        value = cookies.get(self.key, None)
        if value is None:
            return False
        data = json.loads(self.decrypt(value))
        if not isinstance(data, dict):
            return False
        self.store = data
        self.update(self.store)

    def create_signature(self, value, timestamp):
        h = hmac.new(self.secret.encode(), digestmod=hashlib.sha1)
        h.update(timestamp)
        h.update(value)
        return h.hexdigest()

    def encrypt(self, value):
        timestamp = str(int(time.time())).encode()
        value = base64.b64encode(value.encode(self.encoding))
        signature = self.create_signature(value, timestamp)
        return "|".join([value.decode(self.encoding), timestamp.decode(self.encoding), signature])

    def decrypt(self, value):
        value, timestamp, signature = value.split("|")
        check = self.create_signature(value.encode(self.encoding), timestamp.encode())
        if check != signature:
            return None
        return base64.b64decode(value).decode(self.encoding)


class LoginPlugin(object):

    name = 'session'
    api = 2

    def __init__(self):
        self.secret = None
        self.app = None
        self.user_loader = None

    def setup(self, app):
        if 'SECRET_KEY' not in app.config:
            raise ValueError('SECRET_KEY should be setted for use the Session plugin')
        if app.config.get('DEBUG'):
            logger.setLevel('DEBUG')
        self.secret = app.config['SECRET_KEY']

    def create_session(self):
        return BottleSession(self.secret)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            session = self.create_session()
            request.environ['session'] = session
            session.load(request.cookies)
            logging.debug('Started: %s', session)
            result = callback(*args, **kwargs)
            logging.debug('Ended: %s', session)
            session.save(response.set_cookie)
            return result
        return wrapper

    def load_user(self, func):
        self.user_loader = func

    def get_user(self):
        session = request.environ['session']
        user_id = session.get('user_id')
        if not user_id:
            return None
        return self.user_loader(user_id)

    @staticmethod
    def login_user(user_id):
        session = request.environ['session']
        session['user_id'] = user_id
        session.save(response.set_cookie)

    @staticmethod
    def logout_user():
        session = request.environ['session']
        session.pop('user_id', None)
        session.save(response.set_cookie)

    def login_required(self, url=None):
        def decorator(callback):
            def wrapper(*args, **kwargs):
                if self.get_user():
                    return callback(*args, **kwargs)

                if url:
                    return redirect(url)

                return abort(401, "Access denied.")
            return wrapper

        if callable(url):
            callback = url
            url = None
            return decorator(callback)

        return decorator


# pylama:ignore=W0621,W0231,W0404,E0710
