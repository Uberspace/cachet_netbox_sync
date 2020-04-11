# cachet netbox sync

* Fact: host list is stored in [netbox]
* Fact: there is a [cachet] instance
* Fact: you don't want to add hosts manually

* Goal: cachet reports some or all of your hosts

* Solution: cachet_netbox_sync

[netbox]: https://netbox.readthedocs.io/
[cachet]: https://cachethq.io/

## Setup

```console
$ git clone https://github.com/uberspace/cachet_netbox_sync.git
$ make install
```

## Dev Setup

```console
$ git clone https://github.com/uberspace/cachet_netbox_sync.git
$ virtualenv venv
$ source venv/bin/activate
$ make devsetup
```
