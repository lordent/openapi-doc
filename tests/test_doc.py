from openapi_doc import doc
from openapi_doc.base.path import OpenAPIPath

from .fixtures import check_method_spec, fix_doc_settings  # noqa


def test_base_doc_decorators(fix_doc_settings):
    settings = fix_doc_settings

    @doc.summary(settings['summary'])
    @doc.description(settings['description'])
    @doc.operation_id(settings['operation_id'])
    @doc.tags(settings['tags'])
    @doc.deprecated()
    @doc.x(settings['x']['name'], settings['x']['values'])
    @doc.parameter(**settings['integer-parameter'])
    @doc.parameter(**settings['string-parameter'])
    @doc.request(**settings['request'])
    @doc.response(**settings['response'])
    def method():
        pass

    assert hasattr(method, '__openapi__')
    assert isinstance(method.__openapi__, OpenAPIPath)

    spec = method.__openapi__.to_dict()

    check_method_spec(spec, fix_doc_settings)
