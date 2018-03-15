from setuptools import setup


setup(
    name='openapi_doc',
    version='1.0.1',
    author='Vitaliy Nefyodov',
    author_email='vitent@gmail.com',
    url='https://github.com/lordent/openapi_doc',
    description='OpenAPI v3 doc decorators',
    long_description='',
    keywords='openapi openapiv3 swagger sanic',
    packages=[
        'openapi_doc',
        'openapi_doc/base',
        'openapi_doc/base/path',
        'openapi_doc/spec',
    ],
    setup_requires=['marshmallow'],
    tests_require=['tox', 'pytest'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
