FROM python:3

COPY . /usr/src/cachet_netbox_sync
RUN pip install --quiet --no-cache /usr/src/cachet_netbox_sync

ENTRYPOINT ["cachet_netbox_sync"]
