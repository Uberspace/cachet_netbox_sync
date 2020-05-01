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

The tool can be installed conventionally using the python package manager or
newage new age-y using docker.

### Python pip

The easiest way to install this tool is using `pip`, the python package
manager. This will install the dependencies as well as the `cachet_netbox_sync`
command into the python context of the currently logged in user.

```console
$ pip install git+https://github.com/uberspace/cachet_netbox_sync.git
```

### Docker

Alternatively, you can use the [`uberspace/cachet_netbox_sync`](https://hub.docker.com/r/uberspace/cachet_netbox_sync)
docker image to keep the python dependency management off your system.

#### Command

The docker image can be used like a shell command like so:

```console
$ docker pull uberspace/cachet_netbox_sync
$ docker run -V config.ini:/config.ini uberspace/cachet_netbox_sync --config /config.ini
```

#### Custom image

Instead of using our pre-built image, you can make your own. Save the following
snippet as a `Dockerfile`, place a `config.ini` next to it and there you go:
your very own `cachet_netbox_sync` with baked-in config. Just be carefull to not
include any secrets in there, as they can be read by anyone in possession of the
image.

```dockerfile
FROM uberspace/cachet_netbox_sync
COPY config.ini /config.ini
ENTRYPOINT ["cachet_netbox_sync", "-c", "/config.ini"]
```

#### Gitlab

If you have a GitLab with GitLab-CI running, you can use it to refresh your
cachet on-demand or in a cronjob-like fashion.

1. create a new project
2. commit a `config.ini`
3. add your secrets as [variables](https://docs.gitlab.com/ee/ci/variables/#via-the-ui)
4. commit the following `.gitlab-ci.yml`

```yaml
---
sync_cachet:
  image:
    name: uberspace/cachet_netbox_sync
    # https://gitlab.com/gitlab-org/gitlab-runner/issues/1170#note_271904909
    entrypoint: [""]
  script:
    - cachet_netbox_sync --config cachet_netbox_sync.ini
```

## Operation

1. get a cachet API token from `https://cachet.example.com/dashboard/user`
2. get a netbox readonly API token from `https://netbox.example.com/admin/users/token/`
3. copy `config.example.ini` to anywhere (e.g. `~/.cachet_netbox_sync.config.ini`)
   and edit it according to the comments in the file
4. if you decide to leave the API tokens out of the config file, make sure
   `CACHET_TOKEN` and `NETBOX_TOKEN` are defined in the environment you will
   execute `cachet_netbox_sync` from.
5. run `cachet_netbox_sync -c config.ini`. The configuration path must always
   be supplied as a parameter.

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
