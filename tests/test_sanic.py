import pytest
from openapi_spec_validator import validate_spec
from sanic import Sanic, response
from sanic.views import HTTPMethodView
from openapi_doc.spec.sanic import OpenAPISanic
from openapi_doc import doc

from .fixtures import check_method_spec, fix_doc_settings  # noqa


@pytest.yield_fixture
def fix_app(fix_doc_settings):
    app = Sanic('test_sanic_app', strict_slashes=True)

    @doc.description('Test parameter int')
    @app.route('/test-parameter-int/<parameter:int>')
    async def test_parameter_int(request, parameter):
        return response.json({parameter: parameter})

    @doc.description('Test parameter number')
    @app.route('/test-parameter-number/<parameter:number>')
    async def test_parameter_number(request, parameter):
        return response.json({parameter: parameter})

    @doc.description('Test parameter regexp')
    @app.route('/test-parameter-regexp/<parameter:[A-z]+>')
    async def test_parameter_regexp(request, parameter):
        return response.json({parameter: parameter})

    @doc.parameter(in_='path', name='parameter', type_=str, description='Test description')
    @app.route('/test-parameter-replace/<parameter>')
    async def test_parameter_replace(request, parameter):
        return response.json({parameter: parameter})

    @doc.summary(fix_doc_settings['summary'])
    @doc.description(fix_doc_settings['description'])
    @doc.operation_id(fix_doc_settings['operation_id'])
    @doc.tags(fix_doc_settings['tags'])
    @doc.deprecated()
    @doc.x(fix_doc_settings['x']['name'], fix_doc_settings['x']['values'])
    @doc.parameter(**fix_doc_settings['integer-parameter'])
    @doc.parameter(**fix_doc_settings['string-parameter'])
    @doc.request(**fix_doc_settings['request'])
    @doc.response(**fix_doc_settings['response'])
    @app.route('/test_doc')
    async def test_parameter_regexp(request):
        return response.json({'success': True})

    class TestHTTPMethodView(HTTPMethodView):
        @doc.summary(fix_doc_settings['summary'])
        @doc.description(fix_doc_settings['description'])
        @doc.operation_id(fix_doc_settings['operation_id'])
        @doc.tags(fix_doc_settings['tags'])
        @doc.deprecated()
        @doc.x(fix_doc_settings['x']['name'], fix_doc_settings['x']['values'])
        @doc.parameter(**fix_doc_settings['integer-parameter'])
        @doc.parameter(**fix_doc_settings['string-parameter'])
        @doc.request(**fix_doc_settings['request'])
        @doc.response(**fix_doc_settings['response'])
        async def post(self, request):
            return response.json({'success': True})

    app.add_route(TestHTTPMethodView.as_view(), '/test_view_doc')

    yield app


@pytest.fixture
def fix_test_client(loop, fix_app, test_client):
    return loop.run_until_complete(test_client(fix_app))


@pytest.fixture
def fix_spec(fix_app):
    return OpenAPISanic(app=fix_app).to_dict()


def test_validate_spec(fix_spec):
    validate_spec(fix_spec)


async def test_route_handler(fix_spec, fix_doc_settings, fix_test_client):
    spec = fix_spec['paths']['/test_doc']['get']
    check_method_spec(spec, fix_doc_settings)

    resp = await fix_test_client.get('/test_doc')
    assert resp.status == 200
    assert await resp.json() == {'success': True}


async def test_route_view(fix_spec, fix_doc_settings, fix_test_client):
    spec = fix_spec['paths']['/test_view_doc']['post']
    check_method_spec(spec, fix_doc_settings)

    resp = await fix_test_client.post('/test_view_doc')
    assert resp.status == 200
    assert await resp.json() == {'success': True}


def test_route_parameters(fix_spec):
    spec_parameters = fix_spec['paths']['/test-parameter-int/{parameter}']['get']['parameters']
    assert len(spec_parameters) == 1
    spec = spec_parameters[0]
    assert spec == {
        'name': 'parameter',
        'in': 'path',
        'description': 'int',
        'required': True,
        'deprecated': False,
        'allowEmptyValue': False,
        'schema': {
            'type': 'integer'
        },
    }

    spec_parameters = fix_spec['paths']['/test-parameter-number/{parameter}']['get']['parameters']
    assert len(spec_parameters) == 1
    spec = spec_parameters[0]
    assert spec == {
        'name': 'parameter',
        'in': 'path',
        'description': 'number',
        'required': True,
        'deprecated': False,
        'allowEmptyValue': False,
        'schema': {
            'type': 'number'
        },
    }

    spec_parameters = fix_spec['paths']['/test-parameter-regexp/{parameter}']['get']['parameters']
    assert len(spec_parameters) == 1
    spec = spec_parameters[0]
    assert spec == {
        'name': 'parameter',
        'in': 'path',
        'description': '[A-z]+',
        'required': True,
        'deprecated': False,
        'allowEmptyValue': False,
        'schema': {
            'type': 'string'
        },
    }

    spec_parameters = fix_spec['paths']['/test-parameter-replace/{parameter}']['get']['parameters']
    assert len(spec_parameters) == 1
    spec = spec_parameters[0]
    assert spec == {
        'name': 'parameter',
        'in': 'path',
        'description': 'Test description',
        'required': False,
        'deprecated': False,
        'allowEmptyValue': False,
        'schema': {
            'type': 'string'
        },
    }
