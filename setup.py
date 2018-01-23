from distutils.core import setup


setup(
    name='openapi_doc',
    version='0.1a',
    description='OpenAPI v3 doc decorators',
    long_description='',
    author='Vitaliy Nefyodov',
    author_email='vitent@gmail.com',
    packages=['openapi_doc', 'openapi_doc/doc'],
    requires=['marshmallow'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
