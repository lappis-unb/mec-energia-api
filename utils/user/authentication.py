import string
import random

from mec_energia import settings

def generate_random_password():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))

def create_token_response(token, user_id, user_email, user_first_name, user_last_name, user_type):
    response = {
            'token': token,
            'user': {
                'id': user_id,
                'email': user_email,
                'firstName': user_first_name,
                'lastName': user_last_name,
                'type': user_type,
            }
        }

    return response

def create_valid_token_response(is_valid_token):
    response = {
        'is_valid_token': is_valid_token
    }

    return response

def generate_link_to_reset_password(token, user_first_name):
    endpoint_string = f'{settings.MEC_ENERGIA_URL}/{settings.MEC_ENERGIA_PASSWORD_ENDPOINT}/'
    user_first_name = f'?nome={user_first_name}'
    token_string = f'&token={token}'
    
    return endpoint_string + user_first_name + token_string