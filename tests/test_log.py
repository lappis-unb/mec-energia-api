import logging
import logging.config
import pytest
from django.conf import settings
from pathlib import Path

@pytest.fixture
def django_settings(settings):
    settings.LOG_LEVEL = 'DEBUG'
    settings.LOG_DIR = Path('logs')
    settings.LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'level': settings.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file': {
                'level': settings.LOG_LEVEL,
                'class': 'logging.FileHandler',
                'filename': settings.LOG_DIR / 'django.log',
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': settings.LOG_LEVEL,
                'propagate': True,
            },
        },
    }
    return settings

def test_logging_configuration(django_settings):
    logging.config.dictConfig(django_settings.LOGGING)

    logger = logging.getLogger('django')

    assert logger.level == logging.DEBUG

    console_handler = next(
        handler for handler in logger.handlers if isinstance(handler, logging.StreamHandler)
    )
    assert console_handler.level == logging.DEBUG

    file_handler = next(
        handler for handler in logger.handlers if isinstance(handler, logging.FileHandler)
    )
    assert file_handler.level == logging.DEBUG
    assert file_handler.baseFilename.endswith('django.log')

def test_logging_output(django_settings, caplog):
    logging.config.dictConfig(django_settings.LOGGING)

    logger = logging.getLogger('django')

    test_message = "Esta é uma mensagem de log de teste."
    with caplog.at_level(logging.DEBUG):
        logger.debug(test_message)

    assert test_message in caplog.text

    log_file_path = django_settings.LOG_DIR / 'django.log'
    assert log_file_path.exists()

    with open(log_file_path, 'r') as log_file:
        log_contents = log_file.read()
        assert test_message in log_contents

def test_logging_levels(django_settings, caplog):
    logging.config.dictConfig(django_settings.LOGGING)
    logger = logging.getLogger('django')

    messages = {
        'debug': "Mensagem de debug",
        'info': "Mensagem de informação",
        'warning': "Mensagem de aviso",
        'error': "Mensagem de erro",
        'critical': "Mensagem crítica",
    }

    for level, message in messages.items():
        with caplog.at_level(getattr(logging, level.upper())):
            getattr(logger, level)(message)

        assert message in caplog.text

def test_log_file_creation(django_settings):
    log_file_path = django_settings.LOG_DIR / 'django.log'
    logging.config.dictConfig(django_settings.LOGGING)

    assert log_file_path.exists()

def test_log_directory_exists(django_settings):
    log_dir = django_settings.LOG_DIR
    log_dir.mkdir(parents=True, exist_ok=True)  # Cria o diretório se não existir

    assert log_dir.exists()

def test_logger_handlers_removal(django_settings):
    logging.config.dictConfig(django_settings.LOGGING)
    logger = logging.getLogger('django')

    # Remover todos os manipuladores
    logger.handlers.clear()
    assert len(logger.handlers) == 0

def test_logging_format(django_settings, caplog):
    logging.config.dictConfig(django_settings.LOGGING)
    logger = logging.getLogger('django')

    test_message = "Mensagem de teste para formatação."
    with caplog.at_level(logging.DEBUG):
        logger.debug(test_message)

    assert "DEBUG" in caplog.text  # Verifica se o nível está presente
    assert "Mensagem de teste para formatação." in caplog.text