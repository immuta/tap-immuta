#!/usr/bin/env python3

import singer

from tap_immuta.client import ImmutaClient
from tap_immuta.runner import Runner
from tap_immuta.streams import AVAILABLE_STREAMS

LOGGER = singer.get_logger()  # noqa


class immutaRunner(Runner):
    pass


@singer.utils.handle_top_exception(LOGGER)
def main():
    args = singer.utils.parse_args(required_config_keys=['api-key'])
    client = ImmutaClient(args.config)
    runner = immutaRunner(args, client, AVAILABLE_STREAMS)

    if args.discover:
        runner.do_discover()
    else:
        runner.do_sync()


if __name__ == '__main__':
    main()