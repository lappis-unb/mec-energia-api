from mec_energia import settings

MEC_ENERGIA_URL = settings.MEC_ENERGIA_URL

def template_email_first_access(user_name, university_name, link_reset_password_page):
    title = 'Cadastro Universidades Sustentáveis'

    message = f'''
        == Esta é uma mensagem automática, não é necessário responder ==

        <p>Olá {user_name},</p>
        
        <p>Seu cadastrado foi criado no sistema Universidades Sustentáveis para análise do contrato de fornecimento de energia da(o) {university_name}.</p>

        Para acessar o sistema, cadastre uma senha clicando no link abaixo:<br>
        {link_reset_password_page}

        <p>Se nem você, nem a sua chefia imediata solicitaram o cadastro, você pode responder esta mensagem e pedir o cancelamento.</p>

        <p>Tenha um bom dia.</p>

        == Esta é uma mensagem automática, não é necessário responder ==
    '''

    return (title, message)

def template_email_recovery_password(user_name, link_reset_password_page):
    title = 'Redefinição de senha - Universidades Sustentáveis'

    message = f'''
        == Esta é uma mensagem automática, não é necessário responder ==

        <p>Olá {user_name},</p>

        <p>Você solicitou a redefinição da sua senha de acesso ao sistema Universidades Sustentáveis.</p>

        Para criar uma nova senha, clique no link abaixo:<br>
        {link_reset_password_page}

        <p>Se você não solicitou a redefinição da senha, ignore esta mensagem.</p>

        <p>Tenha um bom dia.</p>

        == Esta é uma mensagem automática, não é necessário responder ==
    '''

    return (title, message)

def template_email_recovery_password_by_admin(user_name, link_reset_password_page):
    title = 'Redefinição de senha - Universidades Sustentáveis'

    message = f'''
        == Esta é uma mensagem automática, não é necessário responder ==

        <p>Olá {user_name},</p>

        <p>A redefinição da sua senha de acesso ao sistema Universidades Sustentáveis foi realizada pela administração do sistema. Sua senha atual foi desativada.</p>

        Para criar uma nova senha, clique no link abaixo:<br>
        {link_reset_password_page}

        <p>Tenha um bom dia.</p>

        == Esta é uma mensagem automática, não é necessário responder ==
    '''

    return (title, message)