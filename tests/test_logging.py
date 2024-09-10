import pytest
import io
import logging
from django.conf import settings

@pytest.fixture
def logger():
    logger = logging.getLogger('test_logger')
    logger.setLevel(logging.DEBUG)
    capture_string = io.StringIO();
    handler = logging.StreamHandler(capture_string)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    yield logger, capture_string
    logger.handlers.clear()

def test_logging_configuration():
    assert hasattr(settings, 'LOGGING'), "A configuração de logging deve estar presente nos settings do Django"
    assert 'handlers' in settings.LOGGING, "A configuração de logging deve definir handlers"
    assert 'console' in settings.LOGGING['handlers'], "A configuração de logging deve definir um handler 'console'"

def test_logging_debug(logger):
    logger, capture_string = logger
    logger.debug("Teste de log de DEBUG")
    assert "Teste de log de DEBUG" in capture_string.getvalue()

def test_logging_info(logger):
    logger, capture_string = logger
    logger.info("Teste log de informação")
    assert "Teste log de informação" in capture_string.getvalue()

def test_logging_warning(logger):
    logger, capture_string = logger
    logger.warning("Teste log de aviso")
    assert "Teste log de aviso" in capture_string.getvalue()

def test_logging_error(logger):
    logger, capture_string = logger
    logger.error("Teste log de erro")
    assert "Teste log de erro" in capture_string.getvalue()

def test_logging_critical(logger):
    logger, capture_string = logger
    logger.critical("Teste de log crítico")
    assert "Teste de log crítico" in capture_string.getvalue()