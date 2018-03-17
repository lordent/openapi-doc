class OpenAPIPath:

    def __init__(self):
        self.summary = None
        self.description = None
        self.operation_id = None
        self.deprecated = None
        self.parameters = list()
        self.path_parameters = list()
        self.tags = None
        self.request = None
        self.responses = dict()
        self.schemas = set()
        self.x = dict()

    def to_dict(self):
        return dict(
            filter(lambda item: not item[1] is None, [
                ('summary', self.summary),
                ('description', self.description),
                ('operationId', self.operation_id),
                ('deprecated', self.deprecated),
                ('parameters', self.parameters + self.path_parameters),
                ('requestBody', self.request or None),
                ('responses', self.responses),
                ('tags', self.tags),
            ]),
            **{
                'x-%s' % name: list(map(str, args))
                for name, args in self.x.items()
            }
        )
