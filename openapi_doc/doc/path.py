class OpenAPIPath:

    def __init__(self):
        self.summary = ''
        self.description = ''
        self.operation_id = ''
        self.deprecated = False
        self.parameters = list()
        self.tags = list()
        self.responses = dict()
        self.schemas = set()

    def to_dict(self):
        return dict(
            summary=self.summary,
            description=self.description,
            operationId=self.operation_id,
            deprecated=self.deprecated,
            parameters=self.parameters,
            responses=self.responses,
            tags=self.tags,
        )


class OpenAPIPathParameter:
    def __init__(self, name='', in_='', description='', required=False,
                 deprecated=False, allow_empty_value=False, type_=str):
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
    def __init__(self, schema, array=False, status=200, description='', content='application/json'):
        self.schema = schema
        self.array = array
        self.status = status
        self.description = description
        self.content = content

    def to_dict(self):
        if hasattr(self.schema, '__name__'):
            ref = {'$ref': '#/components/schemas/' + self.schema.__name__}
        else:
            ref = {'type': 'string'}
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


def openapi(func):
    if not hasattr(func, '__openapi__'):
        func.__openapi__ = OpenAPIPath()
    return func.__openapi__


def summary(summary_=''):
    def inner(func):
        openapi(func).summary = summary_
        return func
    return inner


def description(description_=''):
    def inner(func):
        openapi(func).description = description_
        return func
    return inner


def operation_id(operation_id_=''):
    def inner(func):
        openapi(func).operation_id = operation_id_
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


def response(schema, array=False, status=200, description='', content='application/json'):
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
