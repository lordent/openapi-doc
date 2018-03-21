from marshmallow.schema import Schema


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
        if isinstance(self.schema, dict):
            ref = self.schema
        if self.array:
            ref = {
                'type': 'array',
                'items': ref,
            }
        return {
            'description': self.description,
            'content': {
                self.content: {'schema': ref},
            },
        }
