class OpenAPIPathParameter:
    def __init__(self, name, in_, description, required, deprecated, allow_empty_value, type_):
        self.name = name
        self.in_ = in_
        self.description = description
        self.required = required
        self.deprecated = deprecated
        self.allow_empty_value = allow_empty_value
        self.type = self.get_type(type_)

    @staticmethod
    def get_type(value):
        if value is int:
            return 'integer'
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
                'type': self.type
            },
        }
