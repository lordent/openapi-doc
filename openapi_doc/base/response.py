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
