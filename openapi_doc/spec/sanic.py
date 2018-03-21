import re

from marshmallow.schema import Schema

from ..base.path.parameter import OpenAPIPathParameter
from ..base.schema import schema_to_dict

from .spec import OpenAPI


class OpenAPISanic(OpenAPI):

    def __init__(self, app, url_prefix='', *args, **kwargs):
        self.app = app
        self.url_prefix = url_prefix

        super(OpenAPISanic, self).__init__(*args, **kwargs)

    def add_method_handler(self, uri, path_parameters, method_name, handler):
        if hasattr(handler, '__openapi__'):
            api_doc = handler.__openapi__
            api_doc.parameters_path = {
                **path_parameters,
                **api_doc.parameters_path
            }

            self.paths[uri][method_name] = api_doc.to_dict()

            for schema in api_doc.schemas:
                if isinstance(schema, Schema):
                    self.schemas.update(
                        **schema_to_dict(schema, relations=self.schemas)
                    )

    def to_dict(self):
        # Collect paths
        methods = ('get', 'post', 'put', 'patch', 'delete')
        for uri, route in self.app.router.routes_all.items():

            if not uri.startswith(self.url_prefix):
                continue

            uri_parsed = uri[len(self.url_prefix):]
            if uri_parsed[0] != '/':
                uri_parsed = '/' + uri_parsed

            path_parameters = dict()

            for parameter in route.parameters:
                description = re.compile('<' + parameter.name + ':([^>]+)>').findall(uri_parsed)
                if description:
                    description = description.pop()

                uri_parsed = re.sub('<' + parameter.name + '.*?>', '{' + parameter.name + '}', uri_parsed)

                path_parameters[parameter.name] = OpenAPIPathParameter(
                    name=parameter.name,
                    in_='path',
                    description=description,
                    required=True,
                    deprecated=False,
                    allow_empty_value=False,
                    type_=parameter.cast,
                )

            self.paths[uri_parsed] = dict()

            if hasattr(route.handler, 'view_class'):
                view = route.handler.view_class
                for method_name in methods:
                    if hasattr(view, method_name):
                        self.add_method_handler(
                            uri_parsed, path_parameters,
                            method_name, getattr(view, method_name)
                        )
            else:
                for method_name in methods:
                    if method_name.upper() in route.methods:
                        self.add_method_handler(
                            uri_parsed, path_parameters,
                            method_name, route.handler
                        )

            if not self.paths[uri_parsed]:
                del self.paths[uri_parsed]

        return super(OpenAPISanic, self).to_dict()
