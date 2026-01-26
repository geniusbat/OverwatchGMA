

from rest_framework.authtoken.models import Token
from enum import Enum
from rest_framework.authentication import get_authorization_header
from  web.models import TokenLogs, DelegateToken


class TOKEN_TYPES(Enum):
    DELEGATE = "delegate token"
    USER = "user token"
    NONE = "not valid token"

def _extract_ip(request)->str:
    ip = request.META["REMOTE_ADDR"]
    #Get ip from X-Forwarded-For, if not just keep it from request
    if "HTTP_X_FORWARDED_FOR" in request.META.keys():
        ip = request.META["HTTP_X_FORWARDED_FOR"]
    return ip

#Extract token and its type
def get_token_and_type(request):
    auth = get_authorization_header(request).split()
    token = auth[1].decode()
    try:
        token = DelegateToken.objects.get(key=token)
        return (token, TOKEN_TYPES.DELEGATE)
    except DelegateToken.DoesNotExist:
        #If it fails then try with default drf token (used by users)
        try:
            token = Token.objects.select_related('user').get(key=token)
            return (token, TOKEN_TYPES.USER)
        except Token.DoesNotExist:
            return (token, TOKEN_TYPES.NONE)

#Log token actions for auditing
def handle_log_token_actions(request, msg:str):
    token, token_type = get_token_and_type(request)
    ip = _extract_ip(request)
    TokenLogs.objects.create(
        ip = ip,
        token_type = token_type.value,
        token = token,
        log = msg
    )