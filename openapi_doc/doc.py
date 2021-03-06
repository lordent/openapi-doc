from .base.path import OpenAPIPath
from .base.path.parameter import OpenAPIPathParameter
from .base.request import OpenAPIRequest
from .base.response import OpenAPIResponse


def openapi(func):
    if not hasattr(func, '__openapi__'):
        func.__openapi__ = OpenAPIPath()
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


def tags(tags):
    def inner(func):
        openapi(func).tags = list(map(str, tags))
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
        if in_ in ('query', 'path', 'header', 'cookie'):
            getattr(
                openapi(func),
                'parameters_%s' % in_
            )[name] = OpenAPIPathParameter(
                name=name,
                in_=in_,
                description=description,
                required=required,
                deprecated=deprecated,
                allow_empty_value=allow_empty_value,
                type_=type_,
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
        )
        return func
    return inner


def response(schema=str, array=False, status=200, description='', content='application/json'):
    def inner(func):
        openapi(func).schemas.add(schema)
        openapi(func).responses[status] = OpenAPIResponse(
            schema=schema,
            array=array,
            status=status,
            description=description,
            content=content,
        )
        return func
    return inner


def x(name, values):
    def inner(func):
        openapi(func).x[name] = values
        return func
    return inner
