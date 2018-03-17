from setuptools import setup


test_deps = [
    'tox',
    'pytest',
    'openapi-spec-validator',
    'sanic',
    'pytest-sanic',
]

extras = {
    'test': test_deps,
}

setup(
    name='openapi_doc',
    version='1.0.0',
    author='Vitaliy Nefyodov',
    author_email='vitent@gmail.com',
    url='https://github.com/lordent/openapi_doc',
    description='OpenAPI v3 doc decorators',
    long_description='',
    keywords='openapi openapi3 openapiv3 swagger sanic',
    packages=[
        'openapi_doc',
        'openapi_doc/base',
        'openapi_doc/base/path',
        'openapi_doc/spec',
    ],
    install_requires=['marshmallow'],
    tests_require=test_deps,
    extras_require=extras,
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
