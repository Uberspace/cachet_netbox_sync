import typing

import cachetclient
import cachetclient.v1.enums as enums  # NOQA

ApiClient = cachetclient.Client


def get_client(url: str, token: str) -> ApiClient:
    cachet = cachetclient.Client(endpoint=url, api_token=token)
    cachet.ping()
    return cachet


def add_groups(client: ApiClient, cachet_groups, netbox_groups):
    to_delete = cachet_groups.copy()
    name_to_id = {}

    for group in netbox_groups:
        if group in cachet_groups:
            name_to_id[group] = cachet_groups[group].id
            del to_delete[group]
        else:
            name_to_id[group] = client.component_groups.create(name=group).id

    return name_to_id, to_delete


def delete_groups(client: ApiClient, group_ids: typing.List[int]):
    for gid in group_ids:
        client.component_groups.delete(gid)


def update_component(component, new_data):
    has_changed = False

    for k, v in new_data.items():
        if v != getattr(component, k):
            setattr(component, k, v)
            has_changed = True

    if has_changed:
        component.update()


def create_component(client, data):
    data = data.copy()
    # cachet returns a set() but only accepts a string
    data['tags'] = ','.join(data['tags'])
    client.components.create(**data)


def delete_components(client: ApiClient, component_ids: typing.List[int]):
    for cid in component_ids:
        client.components.delete(cid)


def upsert_components(client, netbox_components, cachet_components, groupname_to_id):
    to_delete = cachet_components.copy()

    for component in netbox_components:
        name = component['name']
        data = {
            'name': name,
            'status': enums.COMPONENT_STATUS_OPERATIONAL,
            'description': component['description'],
            'tags': {'cachet-netbox-sync'},
            'group_id': groupname_to_id[component['group']],
        }

        if name in cachet_components:
            component = cachet_components[name]
            update_component(component, data)
            del to_delete[name]
        else:
            create_component(client, data)

    return to_delete
