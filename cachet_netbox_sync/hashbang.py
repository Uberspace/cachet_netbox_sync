import os
import sys
from argparse import ArgumentParser

from . import cachet
from . import config
from . import netbox


def main():
    parser = ArgumentParser()
    parser.add_argument('--config-file', '-c', required=True)
    args = parser.parse_args()

    cfg = config.parse(args.config_file, os.environ)
    rc = run_config(cfg)
    sys.exit(rc)


def run_config(cfg):
    netbox_client = netbox.get_client(cfg.netbox.url, cfg.netbox.token)
    cachet_client = cachet.get_client(cfg.cachet.url, cfg.cachet.token)

    netbox_components, netbox_groups = netbox.get_data(netbox_client, cfg.sources)
    cachet_groups = {g.name: g for g in cachet_client.component_groups.list()}
    cachet_components = {
        component.name: component
        for component in cachet_client.components.list()
        if 'cachet-netbox-sync' in component.tags
    }

    groupname_to_id, group_delete_failed = sync_groups(
        cfg, cachet_client, cachet_groups, netbox_groups
    )

    component_delete_failed = sync_components(
        cfg, cachet_client, netbox_components, cachet_components, groupname_to_id
    )

    if group_delete_failed or component_delete_failed:
        return 1
    else:
        return 0


def sync_groups(cfg, cachet_client, cachet_groups, netbox_groups):
    groupname_to_id, groups_to_delete = cachet.add_groups(
        cachet_client, cachet_groups, netbox_groups)
    group_delete_failed = False

    if cfg.unknown_group_action == config.UnknownGroupAction.delete:
        if len(groups_to_delete) <= cfg.group_delete_limit:
            cachet.delete_groups(cachet_client, groups_to_delete.values())
        elif cfg.group_delete_limit_fail:
            group_delete_failed = True

    return groupname_to_id, group_delete_failed


def sync_components(cfg, cachet_client, netbox_components, cachet_components, groupname_to_id):
    component_delete_failed = False

    components_to_delete = cachet.upsert_components(
        cachet_client, netbox_components, cachet_components, groupname_to_id)

    if len(components_to_delete) <= cfg.component_delete_limit:
        cachet.delete_components(cachet_client, components_to_delete)
    elif cfg.component_delete_limit_fail:
        component_delete_failed = True

    return component_delete_failed
