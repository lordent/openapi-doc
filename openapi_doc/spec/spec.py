class OpenAPI:

    def __init__(self, **kwargs):
        self.paths = dict()
        self.schemas = dict()

        self.components = dict(
            schemas=self.schemas,
        )

        self.spec = {
            'openapi': '3.0.0',
            'paths': self.paths,
            'components': self.components,
            **kwargs
        }
