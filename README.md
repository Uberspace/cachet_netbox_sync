# cachet netbox sync

An application to import [netbox] data (circuits, virtual machines, sites, IP
adresses, tenants, clusters, ...) into [cachet]. It saves you from manually
updating your status page inventory when you add a new component to report
status on. All entries can be filtered and grouped arbitrarily as configurated
in a simple plain-text file - no code necessary.

```ini
[source.netbox.u6]
endpoint=virtualization.virtual_machines
filters.tenant=uberspace-6
filters.status=1
group_by_field=tenant.name
```

This example will fetch all active VMs beloning to Uberspace 6, put them into a
group called "Uberspace 6" and display their status on your cachet instance.

[netbox]: https://netbox.readthedocs.io/
[cachet]: https://cachethq.io/

## Setup

The easiest way to install this tool is to get the source and run
`make install`. This will install the dependencies as well as the
`cachet_netbox_sync` into the python context of the currently logged in user.

```console
$ git clone https://github.com/uberspace/cachet_netbox_sync.git
$ make install
```

## Operation

1. get a cachet API token by visiting `/dashboard/user`
2. get a netbox readonly API token by visiting `/admin/users/token/`
3. copy `config.example.ini` and edit it according to the docs below
4. if you decided to leave the API tokens out of the config file, make sure
   `CACHET_TOKEN` and `NETBOX_TOKEN` are defined in your environment.
5. run `cachet_netbox_sync -c config.ini`

### Syncing

The tool syncs two types of objects: components (e.g. VMs, network or sites)
and component groups. In both cases data is taken from netbox to cachet, never
the other way around.

#### Components

* imports netbox data specified `[source.netbox.*]` sections into cachet
* deletes all components, which are not present in netbox
* deletes only if there are fewer or equal to `component_delete_limit`
  components to be deleted
* only touches components which have the `cachet-netbox-sync` tag, so you can
  create additional components in the cachet web interface.

#### Component Groups

* creates all groups implicitly specified via `group_by_field` in sources
* deletes (or keeps) groups, which are not present in netbox, depending on the
  `unknown_group_action` setting
* just like components, there is a `group_delete_limit` setting

### Configuration

Please refer to the comments in [`config.example.ini`](config.example.ini) for
details on how to configure syncing.

### Automation

Once there is a working configuration, a cronjob can be used to sync
the data regularily. The script can also be executed by your CI/CD system
or anything else you use internally.

Add the follwing to the crontab of the user you ran `make install` as:

```cron
0 * * * * cachet_netbox_sync -c ~/.cachet_netbox_sync.config.ini
```

This assumes your `$PATH` includes `~/.local/bin`, which is where pip
installs python "binaries".

## Dev Setup

```console
$ git clone https://github.com/uberspace/cachet_netbox_sync.git
$ cd cachet_netbox_sync
$ virtualenv venv
$ source venv/bin/activate
$ make devsetup
```

To actually run the tool you will need netbox and cachet instances as well as a
configuration file.
