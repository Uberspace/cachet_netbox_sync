.PHONY: \
	clean setup setup-venv setup-requirements setup-pre-commit \
	upgrade lint audit build run test release

IMAGE_NAME ?= localhost/uberspace/compile
IMAGE_TAG ?= latest
IMAGE_FULL_NAME = $(IMAGE_NAME):$(IMAGE_TAG)

PYTHON_DEV_VERSION = $(strip $(shell cat runtime.txt))

ifeq ($(CI), true)

setup: setup-requirements setup-pre-commit

else

VENV := $(shell pwd)/.venv
export PATH := $(VENV)/bin:$(PATH)

clean:
	rm -rf '$(VENV)'

setup: clean setup-venv setup-requirements setup-pre-commit

setup-venv:
	'/usr/bin/python$(PYTHON_DEV_VERSION)' -m venv '$(VENV)'

endif

setup-requirements:
	'pip$(PYTHON_DEV_VERSION)' install --isolated --no-input --quiet \
		-c requirements.txt \
		-r requirements.in

setup-pre-commit:
	pre-commit install --install-hooks

upgrade:
	pip-compile \
		--upgrade \
		--no-header \
		--strip-extras \
		--annotation-style line \
		--output-file - \
		requirements.in \
		$(args) \
	| grep -Fv 'file://$(shell pwd)' > requirements.txt


lint: args := --all-files
lint:
	pre-commit run $(args)

audit:
	@$(MAKE) --no-print-directory \
		lint args="--all-files python-safety-dependencies-check"

build:
	@echo "Building image '$(IMAGE_NAME)' with tag '$(IMAGE_TAG)'"
	docker pull "$(IMAGE_FULL_NAME)" || /bin/true
	docker build \
		--cache-from '$(IMAGE_FULL_NAME)' \
		--tag '$(IMAGE_FULL_NAME)' \
		--tag '$(IMAGE_NAME):latest' \
		.

run:
	@echo "Running image '$(IMAGE_NAME)' with tag '$(IMAGE_TAG)'"
	docker run --rm -it --entrypoint /bin/bash '$(IMAGE_FULL_NAME)'

test:
	@echo "Testing image '$(IMAGE_NAME)' with tag '$(IMAGE_TAG)'"
	docker run --rm '$(IMAGE_FULL_NAME)' cachet_netbox_sync --help

release:
	bumpver update --patch $(args)
