# pylint:disable=all
# flake8: noqa
import copy
import random
import string
from rest_framework import serializers

def get_writable_fields_serializer(original_serializer, exclude=None):
    if not exclude:
        exclude = []
    remove_list = list() + exclude
    fields = original_serializer.Meta.fields
    filtered_list = list()
    try:
        read_only_fields = original_serializer.Meta.read_only_fields
    except AttributeError:
        read_only_fields = list()
    for field in fields:
        if field in read_only_fields:
            remove_list.append(field)
        elif field not in exclude:
            filtered_list.append(field)

    declared_fields = original_serializer.__dict__.copy()
    declared_fields.update(copy.deepcopy(original_serializer._declared_fields))

    try:
        class Meta:
            model = original_serializer.Meta.model
            fields = tuple(filtered_list)

        declared_fields["Meta"] = Meta
    except AttributeError:
        pass

    for item in remove_list:
        if item in declared_fields:
            del declared_fields[item]

    random_chars = "".join([random.choice(string.ascii_letters) for i in range(10)])
    new_serializer = type(original_serializer.__name__+"_writable_"+random_chars, original_serializer.__bases__, declared_fields)
    return new_serializer


def get_readable_fields_serializer(original_serializer):
    remove_list = list()
    fields = original_serializer.Meta.fields
    filtered_list = list()
    try:
        extra_kwargs = original_serializer.Meta.extra_kwargs
    except AttributeError:
        extra_kwargs = dict()

    write_only_fields = list()
    for key, value in extra_kwargs.items():
        if isinstance(value, dict) and "write_only" in value and value["write_only"]:
            write_only_fields.append(key)

    for field in fields:
        if field in write_only_fields:
            remove_list.append(field)
        else:
            filtered_list.append(field)

    declared_fields = original_serializer.__dict__.copy()
    declared_fields.update(copy.deepcopy(original_serializer._declared_fields))
    for item in remove_list:
        if item in declared_fields:
            del declared_fields[item]

    try:
        class Meta:
            model = original_serializer.Meta.model
            fields = tuple(filtered_list)

        declared_fields["Meta"] = Meta
    except AttributeError:
        pass

    random_chars = "".join([random.choice(string.ascii_letters) for i in range(10)])
    new_serializer = type(original_serializer.__name__ + "_readable_" + random_chars, original_serializer.__bases__,
                          declared_fields)
    return new_serializer