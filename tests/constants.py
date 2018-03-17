import pytest


@pytest.fixture
def fix_doc_settings():
    return {
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
            'status': 123,
            'description': 'Test response data description',
            'content': 'application/json',
        },
        'x': {
            'name': 'roles',
            'values': ['admin', 'user']
        },
    }


def check_method_spec(spec, settings):
    assert spec['summary'] == settings['summary']
    assert spec['description'] == settings['description']
    assert spec['operationId'] == settings['operation_id']
    assert spec['deprecated']
    assert spec['tags'] == settings['tags']
    assert spec['x-%s' % settings['x']['name']] == settings['x']['values']

    assert isinstance(spec['parameters'], list)
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

    assert spec['requestBody'] == {
        'description': settings['request']['description'],
        'required': settings['request']['required'],
        'content': {
            settings['request']['content']: {'schema': {'type': 'string'}},
        },
    }

    assert spec['responses'] == {
        str(settings['response']['status']): {
            'description': settings['response']['description'],
            'content': {
                settings['response']['content']: {'schema': {'type': 'string'}},
            },
        },
    }
