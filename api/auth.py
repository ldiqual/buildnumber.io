import base64

from rest_framework import authentication
from rest_framework import exceptions, HTTP_HEADER_ENCODING

from models import Account, ApiKey

class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        token_from_get = request.GET.get('token', None)
        token_from_headers = self._token_from_request_headers(request)

        if token_from_get:
            token = token_from_get
        elif token_from_headers:
            token = token_from_headers
        else:
            msg = "You must provide an API token to use this server. " \
                "You can add `?token=API_TOKEN` at the end of the URL, or use a basic HTTP authentication where user=API_TOKEN with an empty password. " \
                "Please check your emails for your API token."
            raise exceptions.AuthenticationFailed(msg)

        # Grab the API key model, make sure it exists
        try:
            api_key = ApiKey.objects.get(key=token)
        except ApiKey.DoesNotExist:
            raise exceptions.AuthenticationFailed("This API token doesn't exist")

        return (api_key.account, None)


    def _token_from_request_headers(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            msg = _('Invalid basic header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid basic header. Credentials string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError):
            msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
            raise exceptions.AuthenticationFailed(msg)

        return auth_parts[0]
