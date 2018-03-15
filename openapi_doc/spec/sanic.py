import re

from marshmallow.schema import Schema

from ..base.path.parameter import OpenAPIPathParameter
from ..base.schema import schema_to_dict

from .spec import OpenAPI


class OpenAPISanic(OpenAPI):

    def to_dict(self, app, url_prefix=''):
        # Collect paths
        methods = ('get', 'post', 'put', 'patch', 'delete')
        for uri, route in app.router.routes_all.items():

            if not uri.startswith(url_prefix):
                continue

            uri_parsed = uri[len(url_prefix):]
            if uri_parsed[0] != '/':
                uri_parsed = '/' + uri_parsed

            path_parameters = []

            for parameter in route.parameters:
                description = re.compile('<' + parameter.name + ':([^>]+)>').findall(uri_parsed)
                if description:
                    description = description.pop()

                uri_parsed = re.sub('<' + parameter.name + '.*?>', '{' + parameter.name + '}', uri_parsed)

                path_parameters.append(OpenAPIPathParameter(
                    name=parameter.name,
                    in_='path',
                    description=description,
                    required=True,
                    deprecated=False,
                    allow_empty_value=False,
                    type_=parameter.cast,
                ).to_dict())

            self.paths[uri_parsed] = dict()

            if hasattr(route.handler, 'view_class'):
                view = route.handler.view_class
                for method_name in methods:
                    if hasattr(view, method_name):
                        self.paths[uri_parsed][method_name] = dict()
                        handler = getattr(view, method_name)
                        if hasattr(handler, '__openapi__'):
                            api_doc = handler.__openapi__
                            api_doc.path_parameters = path_parameters

                            self.paths[uri_parsed][method_name] = api_doc.to_dict()

                            for schema in api_doc.schemas:
                                if isinstance(schema, Schema):
                                    self.schemas.update(
                                        **schema_to_dict(schema, relations=self.schemas)
                                    )

        return self.spec
