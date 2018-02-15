from marshmallow.schema import Schema


class OpenAPIPath:

    def __init__(self):
        self.summary = ''
        self.description = ''
        self.operation_id = ''
        self.deprecated = False
        self.parameters = list()
        self.path_parameters = list()
        self.tags = list()
        self.request = dict()
        self.responses = dict()
        self.schemas = set()
        self.roles = list()

    def to_dict(self):
        return {
            'summary': self.summary,
            'description': self.description,
            'operationId': self.operation_id,
            'deprecated': self.deprecated,
            'parameters': self.parameters + self.path_parameters,
            'requestBody': self.request,
            'responses': self.responses,
            'tags': self.tags,
            'x-roles': self.roles,
        }


class OpenAPIPathParameter:
    def __init__(self, name, in_, description, required, deprecated, allow_empty_value, type_):
        self.name = name
        self.in_ = in_
        self.description = description
        self.required = required
        self.deprecated = deprecated
        self.allow_empty_value = allow_empty_value
        self.type_ = type_

    def get_type(self):
        if isinstance(self.type_, int):
            return 'int'
        return 'string'

    def to_dict(self):
        return {
            'name': self.name,
            'in': self.in_,
            'description': self.description,
            'required': self.required,
            'deprecated': self.deprecated,
            'allowEmptyValue': self.allow_empty_value,
            'schema': {
                'type': self.get_type()
            },
        }


class OpenAPIResponse:
    def __init__(self, schema, array, status, description, content):
        self.schema = schema
        self.array = array
        self.status = status
        self.description = description
        self.content = content

    def to_dict(self):
        ref = {'type': 'string'}
        if isinstance(self.schema, Schema):
            ref = {'$ref': '#/components/schemas/' + self.schema.__class__.__name__}
        if self.array:
            ref = {
                'type': 'array',
                'items': ref,
            }
        return {
            str(self.status): {
                'description': self.description,
                'content': {
                    self.content: {'schema': ref},
                },
            },
        }


class OpenAPIRequest:
    def __init__(self, schema, required, description, content):
        self.schema = schema
        self.required = required
        self.description = description
        self.content = content

    def to_dict(self):
        ref = {'type': 'string'}
        if isinstance(self.schema, Schema):
            ref = {'$ref': '#/components/schemas/' + self.schema.__class__.__name__}
        return {
            'description': self.description,
            'required': self.required,
            'content': {
                self.content: {'schema': ref},
            },
        }


def openapi(func):
    if not hasattr(func, '__openapi__'):
        func.__openapi__ = OpenAPIPath()
    return func.__openapi__


def roles(*args):
    def inner(func):
        openapi(func).roles += list(map(str, args))
        return func
    return func.__openapi__


def summary(summary):
    def inner(func):
        openapi(func).summary = summary
        return func
    return inner


def description(description):
    def inner(func):
        openapi(func).description = description
        return func
    return inner


def operation_id(operation_id=''):
    def inner(func):
        openapi(func).operation_id = operation_id
        return func
    return inner


def tags(*args):
    def inner(func):
        openapi(func).tags += list(map(str, args))
        return func
    return inner


def deprecated():
    def inner(func):
        openapi(func).deprecated = True
        return func
    return inner


def parameter(
    name='',
    in_='',
    description='',
    required=False,
    deprecated=False,
    allow_empty_value=False,
    type_=str,
):
    def inner(func):
        openapi(func).parameters.append(
            OpenAPIPathParameter(
                name=name,
                in_=in_,
                description=description,
                required=required,
                deprecated=deprecated,
                allow_empty_value=allow_empty_value,
                type_=type_,
            ).to_dict()
        )
        return func
    return inner


def request(schema=str, description='', required=False, content='application/json'):
    def inner(func):
        openapi(func).schemas.add(schema)
        openapi(func).request = OpenAPIRequest(
            schema=schema,
            required=required,
            description=description,
            content=content,
        ).to_dict()
        return func
    return inner


def response(schema=str, array=False, status=200, description='', content='application/json'):
    def inner(func):
        openapi(func).schemas.add(schema)
        openapi(func).responses.update(
            **OpenAPIResponse(
                schema=schema,
                array=array,
                status=status,
                description=description,
                content=content,
            ).to_dict()
        )
        return func
    return inner
