import jwt
import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from .models import token


def generate_access_token(user):
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }
    encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    token_object = token(user=user, user_token=encoded_jwt)
    token_object.save()

    return encoded_jwt.decode('utf-8')


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = None
        if 'jwt' in request.COOKIES:
            token = request.COOKIES.get('jwt')
        # else:
        #     #retreeve from the header
        #     token=token.object.
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('unauthenticated')

        user = get_user_model().objects.filter(id=payload['user_id']).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found!')
        # this will be contained in the request.user
        return (user, None)
