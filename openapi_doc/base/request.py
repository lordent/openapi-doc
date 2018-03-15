from marshmallow.schema import Schema


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
