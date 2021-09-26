import pytest

from datatranslator.app import create_translation_api
from datatranslator.apierror import BadRequest, TranslatorException
from fixtures import DATE_JSON, DATE_RESULT

@pytest.fixture
def app():
    app = create_translation_api()
    app.config["TESTING"] = True
    return app


def test_request_pass(app):
    client = app.test_client()
    response = client.post("/restaurant/dates",json=DATE_JSON)
    assert response.get_json() == DATE_RESULT
    
def test_app_raises_badrequest(app):
    client = app.test_client()
    response = client.post("/restaurant/dates",json=None)
    assert response.status_code == 400
    
def test_app_raises_invalid_type(app):
    app.config['TYPE'] = 2
    client = app.test_client()
    response = client.post("/restaurant/dates",json=DATE_JSON)
    assert response.status_code == 500