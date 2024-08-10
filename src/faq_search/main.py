#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "moz-sec"
__version__ = "0.2.0"
__date__ = "2024/08/10 (Created: 2024/07/19)"

import argparse
import sys

from faq_search.cli import cli_run
from faq_search.server import server_run


def main():
    parser = argparse.ArgumentParser(description="faq search system")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument(
        "query",
        nargs="?",
        help="Search FAQ",
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        default=3,
        help="number of search results",
    )
    parser.add_argument(
        "--server",
        action="store_true",
        default=False,
        help="server mode",
    )
    args = parser.parse_args()

    if args.server:
        server_run()
    else:
        if not args.query:
            parser.error("the following arguments are required: query")

        cli_run(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
