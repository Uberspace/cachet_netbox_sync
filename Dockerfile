FROM python:3
ENV IMAGE_VERSION=2022.05.20
COPY . /usr/src/cachet_netbox_sync
RUN pip install --quiet --no-cache /usr/src/cachet_netbox_sync

ENTRYPOINT ["cachet_netbox_sync"]
