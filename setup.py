from distutils.core import setup


setup(
    name='openapi_doc',
    version='1.0.1',
    description='OpenAPI v3 doc decorators',
    long_description='',
    author='Vitaliy Nefyodov',
    author_email='vitent@gmail.com',
    packages=['openapi_doc', 'openapi_doc/doc'],
    install_requires=['marshmallow'],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
    ]
)
