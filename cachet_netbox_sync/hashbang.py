import sys
from argparse import ArgumentParser
from traceback import print_exc

import cachetclient
import pynetbox


def main():
    parser = ArgumentParser()
    parser.add_argument('--netbox-api-token', required=True)
    parser.add_argument('--cachet-api-token', required=True)
    parser.add_argument('--netbox-url', required=True)
    parser.add_argument('--cachet-api-url', required=True)
    args = parser.parse_args()

    try:
        netbox = pynetbox.api(
            args.netbox_url,
            token=args.netbox_api_token,
            threading=True,
        )
        netbox.version
    except Exception:
        print_exc()
        print('\ncould not connect to nextbox')
        sys.exit(1)

    try:
        cachet = cachetclient.Client(
            endpoint=args.cachet_api_url,
            api_token=args.cachet_api_token,
        )
        cachet.ping()
    except Exception:
        print_exc()
        print('\ncould not connect to cachet')
        sys.exit(1)
