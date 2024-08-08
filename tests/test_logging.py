import logging
import io
import pytest
from django.conf import settings

@pytest.fixture
def logger():
    logger = logging.getLogger('django')
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    yield logger, log_capture_string
    logger.handlers = []

def test_logging_configuration():
    assert hasattr(settings, 'LOGGING'), "A configuração de logging deve estar presente nos settings do Django"
    assert 'handlers' in settings.LOGGING, "A configuração de logging deve definir handlers"
    assert 'console' in settings.LOGGING['handlers'], "A configuração de logging deve definir um handler 'console'"

def test_logging_debug(logger):
    logger, log_capture_string = logger
    logger.debug('Testando log de debug')
    assert 'Testando log de debug' in log_capture_string.getvalue()

def test_logging_info(logger):
    logger, log_capture_string = logger
    logger.info('Testando log de informação')
    assert 'Testando log de informação' in log_capture_string.getvalue()

def test_logging_warning(logger):
    logger, log_capture_string = logger
    logger.warning('Testando log de aviso')
    assert 'Testando log de aviso' in log_capture_string.getvalue()

def test_logging_error(logger):
    logger, log_capture_string = logger
    logger.error('Testando log de erro')
    assert 'Testando log de erro' in log_capture_string.getvalue()

def test_logging_critical(logger):
    logger, log_capture_string = logger
    logger.critical('Testando log crítico')
    assert 'Testando log crítico' in log_capture_string.getvalue()

def test_logging_exception(logger):
    logger, log_capture_string = logger
    try:
        raise ValueError('Exceção de teste')
    except ValueError:
        logger.exception('Testando log de exceção')
    assert 'Testando log de exceção' in log_capture_string.getvalue()
    assert 'ValueError: Exceção de teste' in log_capture_string.getvalue()