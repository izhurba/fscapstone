'''
Code borrowed from coffee_shop_FS project earlier in ND course
'''
import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'dev-vqzjqwjq.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'repairshop'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

# Returns token from proper Authorization request

def get_token_auth_header():
    authHead = request.headers.get('Authorization')
    
    if not authHead:
        raise AuthError({
           'code': 'No Header',
           'description': 'Authorization header not provided'
        }, 401)
    
    authHead = authHead.split(' ')

    if len(authHead) != 2:
        raise AuthError({
           'code': 'Malformed Header',
           'description': 'Improper header length'
        }, 401)
    
    if authHead[0].lower() != 'bearer':
        raise AuthError({
           'code': 'Invalid Header',
           'description': 'Authorization header must start with "bearer"'
        }, 401)
    
    return authHead[1]

# Checks for present permissions string and proper permission in payload

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
           'code': 'No permissions',
           'description': 'Permissions not present in payload'
        }, 401)

    if permission not in payload['permissions']:
        raise AuthError({
           'code': 'Unauthorized',
           'description': 'User does not have required permissions'
        }, 403)

    return True

def verify_decode_jwt(token):
    jUrl = urlopen('https://'+ AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = json.loads(jUrl.read())

    head = jwt.get_unverified_header(token)
    
    if 'kid' not in head:
        raise AuthError({
            'code': 'Invalid Header',
            'description': 'Malformed Authorization Token'
        }, 401)
    
    rsa_key = {}

    for key in jwks['keys']:
        if key['kid'] == head['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            break
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'Expired Token',
                'description': 'Authorization token is expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'Invalid Claims',
                'description': 'Invalid claim. Check audience and issuer'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'Invalid Header',
                'description': 'Unable to parse authentication token'
            }, 400)
    raise AuthError({
        'code': 'Invalid Token',
        'description': 'No proper RSA key found'
    }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return 