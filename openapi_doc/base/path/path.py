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
        self.x = dict()

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
            **{
                'x-%s' % name: list(map(str, args))
                for name, args in self.x.items()
            }
        }

