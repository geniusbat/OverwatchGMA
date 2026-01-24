from rest_framework.authentication import BaseAuthentication, get_authorization_header, exceptions
from django.contrib.auth.models import AnonymousUser

from . import models

#User class used by DelegateTokenAuthentication as it requires an user but no user is actually related to the host_registry
class DelegateAnonymousUser(AnonymousUser):
    is_delegate = True #Attribute used to distingish DelegateAnonymousUser from AnonymousUser
    is_staff = False
    is_admin = False
    @property
    def is_authenticated(self):
        return True

class TokenAuthentication(BaseAuthentication):
    """
    Token based authentication, copied from DRF's TokenAuthentication and modified to use DelegateTokens and DRF Tokens at the same time.

    Clients should authenticate by passing the token key in the "Authorization" HTTP header, prepended with the string "Token ".  For example:
        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'Token'
    tokenModel = models.DelegateToken

    def get_model_delegates(self):
        if self.tokenModel is not None:
            return self.tokenModel
        raise NotImplementedError

    def get_model_users(self):
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        #First try to authenticate with a DelegateToken
        tokenModel = self.get_model_delegates()
        try:
            token = tokenModel.objects.get(key=key)
        except tokenModel.DoesNotExist:
            #If it fails then authenticate with default drf token (used by users)
            tokenModel = self.get_model_users()
            try:
                token = tokenModel.objects.select_related('user').get(key=key)
                #Make sure user is active
                if not token.user.is_active:
                    raise exceptions.AuthenticationFailed('User inactive or deleted.')
                return (token.user, token)
            except tokenModel.DoesNotExist:
                raise exceptions.AuthenticationFailed(('Invalid token.'))
        user = DelegateAnonymousUser() #Get authenticated anonymous user for delegate token
        return (user, token)

    def authenticate_header(self, request):
        return self.keyword
    