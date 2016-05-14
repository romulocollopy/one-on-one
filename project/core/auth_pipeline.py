import json
from social.exceptions import AuthForbidden


def auth_allowed(backend, details, response, *args, **kwargs):
    if not backend.auth_allowed(response, details):
        raise AuthForbidden(backend)
    if not _is_eshares(details['email']):
        raise AuthForbidden(backend)


def _is_eshares(email):
    if "@esharesinc.com" not in email:
        return False
    return True
