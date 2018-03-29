from functools import reduce
import operator


class OpenAPIPath:

    def __init__(self):
        self.summary = None
        self.description = None
        self.operation_id = None
        self.deprecated = None
        self.parameters_query = dict()
        self.parameters_path = dict()
        self.parameters_header = dict()
        self.parameters_cookie = dict()
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
                ('tags', self.tags),
                (
                    'parameters',
                    reduce(
                        operator.concat, list(
                            list(map(
                                lambda p: p.to_dict(), parameters.values()))
                            for parameters in (
                                self.parameters_query,
                                self.parameters_path,
                                self.parameters_header,
                                self.parameters_cookie,
                            )
                        )
                    )
                ),
                (
                    'requestBody',
                    self.request.to_dict() if self.request else None
                ),
                (
                    'responses',
                    {
                        str(status): response.to_dict()
                        for status, response in self.responses.items()
                    }
                ),
            ]),
            **{
                'x-%s' % name: list(map(str, args))
                for name, args in self.x.items()
            }
        )
