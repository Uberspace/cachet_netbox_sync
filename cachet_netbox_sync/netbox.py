import typing

import pynetbox

from .config import SourceConfig
from .util import deepgetattr

ApiType = pynetbox.api


def get_client(url, token) -> ApiType:
    netbox = pynetbox.api(url, token=token, threading=True)
    netbox.version
    return netbox


def _get_source_data(netbox: ApiType, source: SourceConfig):
    source_endpoint = deepgetattr(netbox, source.endpoint)

    if source.filters:
        objs = source_endpoint.filter(**source.filters)
    else:
        objs = source_endpoint.all()

    for obj in objs:
        name = deepgetattr(obj, source.name_field)
        description = deepgetattr(obj, source.description_field)
        group = deepgetattr(obj, source.group_by_field) or source.group

        yield {
            'name': name,
            'description': description or '',
            'group': group,
        }


def get_data(netbox: ApiType, sources: typing.List[SourceConfig]):
    components = [
        component
        for source in sources
        for component in _get_source_data(netbox, source)
    ]

    groups = set(
        obj['group']
        for obj in components
        if obj['group']
    )

    return components, groups
