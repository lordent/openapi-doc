import marshmallow
import copy


FIELD_MAPPING = {
    marshmallow.fields.Integer: ('integer', 'int64'),
    marshmallow.fields.Number: ('number', None),
    marshmallow.fields.Float: ('number', 'float'),
    marshmallow.fields.Decimal: ('double', None),
    marshmallow.fields.String: ('string', None),
    marshmallow.fields.Boolean: ('boolean', None),
    marshmallow.fields.UUID: ('string', 'uuid'),
    marshmallow.fields.DateTime: ('string', 'date-time'),
    marshmallow.fields.Date: ('string', 'date'),
    marshmallow.fields.Time: ('string', None),
    marshmallow.fields.Email: ('string', 'email'),
    marshmallow.fields.URL: ('string', 'url'),
    marshmallow.fields.Dict: ('object', None),
    # Assume base Field and Raw are strings
    marshmallow.fields.Field: ('string', None),
    marshmallow.fields.Raw: ('string', None),
    marshmallow.fields.List: ('array', None),
}


def schema_to_dict(schema, relations=None):
    """
    required:
        - id
        - name
    properties:
        id:
          type: integer
          format: int64
        name:
          type: string
        tag:
          type: string
    :param schema:
    :param relations:
    :return:

    """

    def serialize_fields(schema):
        required = list()
        properties = dict()

        if hasattr(schema, 'fields'):
            fields = schema.fields
        elif hasattr(schema, '_declared_fields'):
            fields = copy.deepcopy(schema._declared_fields)
        else:
            raise ValueError(
                "{0!r} doesn't have either `fields` or `_declared_fields`".format(schema)
            )

        exclude_fields = getattr(getattr(schema, 'Meta', None), 'exclude', [])
        dump_only_fields = getattr(getattr(schema, 'Meta', None), 'dump_only', [])

        for field_name, field_obj in fields.items():
            if (
                field_name in exclude_fields
                or field_obj.dump_only
                or field_name in dump_only_fields
            ):
                continue

            metadata_description = field_obj.metadata.get('description', '')
            metadata_deprecated = field_obj.metadata.get('deprecated', False)
            metadata_format = field_obj.metadata.get('format', '')

            properties[field_name] = {
                'description': metadata_description,
                'deprecated': metadata_deprecated,
            }

            if field_obj.required:
                required.append(field_name)

            if isinstance(field_obj, marshmallow.fields.Nested):
                ref = {'$ref': '#/components/schemas/' + field_obj.nested.__name__}

                if field_obj.many:
                    properties[field_name].update(**{
                        'type': 'array',
                        'items': ref,
                    })
                else:
                    properties[field_name].update(**ref)

                if relations is not None:
                    relations.update(
                        **schema_to_dict(field_obj.nested, relations=relations)
                    )

                continue

            if isinstance(field_obj, marshmallow.fields.List):
                type_, format_ = FIELD_MAPPING.get(type(field_obj.container), ('string', None))

                properties[field_name].update(**{
                    'type': 'array',
                    'items': {
                        'type': type_,
                        'format': metadata_format or format_,
                    },
                })

                continue

            type_, format_ = FIELD_MAPPING.get(type(field_obj), ('string', None))

            properties[field_name].update(**{
                'type': type_,
                'format': metadata_format or format_,
                'nullable': field_obj.allow_none,
            })

        return dict(required=required, properties=properties)

    return {schema.__class__.__name__: serialize_fields(schema)}
