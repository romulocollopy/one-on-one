from djangio.core.exceptions import PermissionDenied


def auth_allowed(backend, details, response, *args, **kwargs):
    if not backend.auth_allowed(response, details):
        raise PermissionDenied(backend)
    if not _is_eshares(details['email']):
        raise PermissionDenied(backend)


def _is_eshares(email):
    if "@esharesinc.com" not in email:
        return False
    return True
