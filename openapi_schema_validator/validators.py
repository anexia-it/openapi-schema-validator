from attr import attrib, attrs
from copy import deepcopy

from jsonschema import _legacy_validators, _utils, _validators
from jsonschema.validators import create, Draft202012Validator, extend

from openapi_schema_validator import _types as oas_types
from openapi_schema_validator import _validators as oas_validators
from openapi_schema_validator._types import oas31_type_checker

BaseOAS30Validator = create(
    meta_schema=_utils.load_schema("draft4"),
    validators={
        u"multipleOf": _validators.multipleOf,
        # exclusiveMaximum supported inside maximum_draft3_draft4
        u"maximum": _legacy_validators.maximum_draft3_draft4,
        # exclusiveMinimum supported inside minimum_draft3_draft4
        u"minimum": _legacy_validators.minimum_draft3_draft4,
        u"maxLength": _validators.maxLength,
        u"minLength": _validators.minLength,
        u"pattern": _validators.pattern,
        u"maxItems": _validators.maxItems,
        u"minItems": _validators.minItems,
        u"uniqueItems": _validators.uniqueItems,
        u"maxProperties": _validators.maxProperties,
        u"minProperties": _validators.minProperties,
        u"enum": _validators.enum,
        # adjusted to OAS
        u"type": oas_validators.type,
        u"allOf": _validators.allOf,
        u"oneOf": _validators.oneOf,
        u"anyOf": _validators.anyOf,
        u"not": _validators.not_,
        u"items": oas_validators.items,
        u"properties": _validators.properties,
        u"required": oas_validators.required,
        u"additionalProperties": oas_validators.additionalProperties,
        # TODO: adjust description
        u"format": oas_validators.format,
        # TODO: adjust default
        u"$ref": _validators.ref,
        # fixed OAS fields
        u"nullable": oas_validators.nullable,
        u"discriminator": oas_validators.not_implemented,
        u"readOnly": oas_validators.readOnly,
        u"writeOnly": oas_validators.writeOnly,
        u"xml": oas_validators.not_implemented,
        u"externalDocs": oas_validators.not_implemented,
        u"example": oas_validators.not_implemented,
        u"deprecated": oas_validators.not_implemented,
    },
    type_checker=oas_types.oas30_type_checker,
    # NOTE: version causes conflict with global jsonschema validator
    # See https://github.com/p1c2u/openapi-schema-validator/pull/12
    # version="oas30",
    id_of=lambda schema: schema.get(u"id", ""),
)

BaseOAS31Validator = extend(
    Draft202012Validator,
    {
        #  adjusted to OAS
        u"description": oas_validators.not_implemented,
        u"format": oas_validators.format,
        # fixed OAS fields
        u"discriminator": oas_validators.not_implemented,
        u"xml": oas_validators.not_implemented,
        u"externalDocs": oas_validators.not_implemented,
        u"example": oas_validators.not_implemented,
    },
    type_checker=oas31_type_checker,
)


@attrs
class OAS30Validator(BaseOAS30Validator):

    read: bool = attrib(default=None)
    write: bool = attrib(default=None)

    def iter_errors(self, instance, _schema=None):
        if _schema is None:
            # creates a copy by value from schema to prevent mutation
            _schema = deepcopy(self.schema)

        # append defaults to trigger validator (i.e. nullable)
        if 'nullable' not in _schema:
            _schema.update({
                'nullable': False,
            })

        validator = self.evolve(schema=_schema)
        return super(OAS30Validator, validator).iter_errors(instance)


class OAS31Validator(BaseOAS31Validator):
    pass
