SRCDIR=cachet_netbox_sync

.PHONY: lint
lint:
	pre-commit run -a

.PHONY: install
setup:
	pip install --user -e .

.PHONY: devsetup
devsetup:
	pip install -e .[dev]
	pre-commit install --overwrite --install-hooks
