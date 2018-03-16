from openapi_doc import doc
from openapi_doc.base.path import OpenAPIPath


def test_base_doc_decorators():
    settings = {
        'summary': 'Test summary text',
        'description': 'Test description text',
        'operation_id': 'test-operation-id',
        'tags': ['test', 'foo', 'bar'],
        'string-parameter': {
            'name': 'test-string-parameter-name',
            'in_': 'path',
            'description': '',
            'required': True,
            'deprecated': False,
            'allow_empty_value': False,
            'type_': str,
        },
        'integer-parameter': {
            'name': 'test-integer-parameter-name',
            'in_': 'path',
            'description': '',
            'required': False,
            'deprecated': True,
            'allow_empty_value': True,
            'type_': int,
        },
        'request': {
            'schema': str,
            'description': 'Test request data description',
            'required': False,
            'content': 'application/json'
        },
        'response': {
            'schema': str,
            'array': False,
            'status': 200,
            'description': 'Test response data description',
            'content': 'application/json',
        },
        'x': {
            'name': 'roles',
            'values': ['admin', 'user']
        },
    }

    @doc.summary(settings['summary'])
    @doc.description(settings['description'])
    @doc.operation_id(settings['operation_id'])
    @doc.tags(settings['tags'])
    @doc.deprecated()
    @doc.x(settings['x']['name'], settings['x']['values'])
    @doc.parameter(**settings['integer-parameter'])
    @doc.parameter(**settings['string-parameter'])
    @doc.request(**settings['request'])
    @doc.response(**settings['response'])
    def method():
        pass

    assert hasattr(method, '__openapi__') is True
    assert isinstance(method.__openapi__, OpenAPIPath) is True

    spec = method.__openapi__.to_dict()

    assert isinstance(spec, dict) is True

    assert spec['summary'] == settings['summary']
    assert spec['description'] == settings['description']
    assert spec['operationId'] == settings['operation_id']
    assert spec['deprecated'] is True
    assert spec['tags'] == settings['tags']
    assert spec['x-%s' % settings['x']['name']] == settings['x']['values']

    assert isinstance(spec['parameters'], list) is True
    assert len(spec['parameters']) == 2

    assert spec['parameters'][0] == {
        'name': settings['string-parameter']['name'],
        'in': settings['string-parameter']['in_'],
        'description': settings['string-parameter']['description'],
        'required': settings['string-parameter']['required'],
        'deprecated': settings['string-parameter']['deprecated'],
        'allowEmptyValue': settings['string-parameter']['allow_empty_value'],
        'schema': {
            'type': 'string'
        },
    }

    assert spec['parameters'][1] == {
        'name': settings['integer-parameter']['name'],
        'in': settings['integer-parameter']['in_'],
        'description': settings['integer-parameter']['description'],
        'required': settings['integer-parameter']['required'],
        'deprecated': settings['integer-parameter']['deprecated'],
        'allowEmptyValue': settings['integer-parameter']['allow_empty_value'],
        'schema': {
            'type': 'integer'
        },
    }

    assert isinstance(spec['requestBody'], dict) is True

    assert spec['requestBody'] == {
        'description': settings['request']['description'],
        'required': settings['request']['required'],
        'content': {
            settings['request']['content']: {'schema': {'type': 'string'}},
        },
    }

    assert isinstance(spec['responses'], dict) is True

    assert spec['responses'] == {
        str(settings['response']['status']): {
            'description': settings['response']['description'],
            'content': {
                settings['response']['content']: {'schema': {'type': 'string'}},
            },
        },
    }
