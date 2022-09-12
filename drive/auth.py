import os
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


class ServerAuth:
    token_keyword = 'Server'

    @classmethod
    def verify_auth_header(cls, request):
        '''
        '''
        token = get_authorization_header(request).split()

        # Ensure keyword is correct
        if not token or token[0].lower() != cls.token_keyword.lower().encode():
            raise AuthenticationFailed('Invalid token keyword.')

        # Ensure token only has 2 parts: keyword & token
        if len(token) == 1:
            msg = 'Invalid authorization header. No token provided.'
            raise AuthenticationFailed(msg)
        elif len(token) > 2:
            msg = 'Invalid authorization header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        # Ensure token is in valid format
        try:
            decoded_token = token[1].decode()
        except UnicodeError:
            msg = 'Invalid authorization header. Token string contains invalid characters.'
            raise AuthenticationFailed(msg)

        # Finally, ensure the token matches
        if not decoded_token or decoded_token != os.getenv('AUTH_TOKEN'):
            raise AuthenticationFailed('Invalid token.')
