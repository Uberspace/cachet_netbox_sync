import configparser
import enum
import os
import typing
from dataclasses import dataclass


@dataclass
class NetboxConfig:
    url: str
    token: str


@dataclass
class CachetConfig:
    url: str
    token: str


class UnknownGroupAction(enum.Enum):
    keep = enum.auto()
    delete = enum.auto()


@dataclass
class SourceConfig:
    endpoint: str
    filters: typing.Dict[str, str]
    group_by_field: str = None
    group: str = None
    name_field: str = 'name'
    description_field: str = ''


@dataclass
class Config:
    netbox: NetboxConfig
    cachet: CachetConfig

    unknown_group_action: UnknownGroupAction

    component_delete_limit: int
    component_delete_limit_fail: bool

    group_delete_limit: int
    group_delete_limit_fail: bool

    sources: typing.List[SourceConfig]


def _parse_smart_section(
    section: configparser.SectionProxy
) -> typing.Dict[str, typing.Union[str, typing.Dict[str, str]]]:
    """
    Convert a ConfigParser section into a python dictionary. Values within the
    section are converted dictionary keys. The section name is ignored. To
    ignore unrelated values any key starting with "env_" is ignored.

    Two types of keys are supported:

        simple keys

            [source]
            url=https://example.org

            => {'url': 'https://example.org'}

        subdict keys

            [source]
            filter.tenant=u6
            filter.status=1

            => {'filter': {'tenant': 'u6', 'status': '1'}}
    """
    data = {}

    for k, v in section.items():
        if k.startswith('env_'):
            continue

        if '.' in k:  # parse subdict value: filter.tenant=u6
            k, _, kk = k.partition('.')
            if k not in data:
                data[k] = {}
            data[k][kk] = v
        else:  # parse simple value: url=https://example.org
            data[k] = v

    return data


def _parse_listsection(
    parser: configparser.ConfigParser,
    prefix: str
) -> typing.Dict[str, typing.Dict[str, str]]:
    """
    Convert multiple sections into an array of dicts.

        [source.u6]
        name=Uberspace 6

        [source.u7]
        name=Uberspace 7

        =>

        {
            'u6': {'name': 'Uberspace 6'},
            'u7': {'name': 'Uberspace 7'},
        }

    The actual section parsing is handled by parse_smart_section().
    """
    prefix = prefix.rstrip('.') + '.'
    sections = {}

    for section_name in parser.sections():
        if section_name.startswith(prefix):
            section = parser[section_name]
            sections[section_name[len(prefix):]] = _parse_smart_section(section)

    return sections


def parse(config_path: str) -> Config:
    env_vars = {f'ENV_{k}': v for k, v in os.environ.items() if '%' not in v}
    parser = configparser.ConfigParser(defaults=env_vars)
    parser.read(config_path)

    return Config(
        netbox=NetboxConfig(
            url=parser['netbox']['url'],
            token=parser['netbox']['token'],
        ),
        cachet=CachetConfig(
            url=parser['cachet']['url'],
            token=parser['cachet']['token'],
        ),
        unknown_group_action=UnknownGroupAction[parser['base']['unknown_group_action']],
        group_delete_limit=parser.getint('base', 'group_delete_limit'),
        component_delete_limit=parser.getint('base', 'component_delete_limit'),
        group_delete_limit_fail=parser.getboolean('base', 'group_delete_limit_fail'),
        component_delete_limit_fail=parser.getboolean('base', 'component_delete_limit_fail'),
        sources=[
            SourceConfig(**s)
            for s in _parse_listsection(parser, 'source.netbox').values()
        ],
    )
