from email_validator import validate_email, EmailNotValidError

def verify_email_is_valid(email):
    try:
        # Validar o e-mail
        validate_email(email, check_deliverability=True).normalized
    except EmailNotValidError as e:
        # O e-mail não é válido, levantar exceção
        raise Exception(f'Email not valid: {e}')

    return True
