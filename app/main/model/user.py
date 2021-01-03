from .. import db,flask_bcrypt
import datetime
from app.main.model.blacklist import BlacklistToken
from ..config import key
import jwt

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255),unique=True,nullable=False)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(100))
    public_id = db.Column(db.String(100), unique=True)
    joined_at = db.Column(db.DateTime, nullable=False)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)


    @staticmethod
    def encode_auth_token(user_id):
        
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            token = jwt.encode(
                payload,
                key,
                'HS256'
            ).decode("utf-8")
            return token
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        
        try:
            payload = jwt.decode(auth_token, key, 'HS256')
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{}'>".format(self.username)