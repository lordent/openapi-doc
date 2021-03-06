class OpenAPI:

    def __init__(self, *args, **kwargs):
        self.paths = dict()
        self.schemas = dict()

        self.components = dict(
            schemas=self.schemas,
        )

        self.spec = {
            'openapi': '3.0.0',
            'info': {
                'title': '',
                'description': '',
                'termsOfService': '',
                'contact': {
                    'name': '',
                    'url': '',
                    'email': '',
                },
                'license': {
                    'name': '',
                    'url': '',
                },
                'version': '',
            },
            'paths': self.paths,
            'components': self.components,
            **kwargs
        }

    def to_dict(self, *args, **kwargs):
        return self.spec
