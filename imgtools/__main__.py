"""Command line interface for image and video processing."""

from argparse import ArgumentParser, RawTextHelpFormatter

from imgtools.tools.__main__ import add_arguments, main


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__, formatter_class=RawTextHelpFormatter)
    parser = add_arguments(parser)
    main(**vars(parser.parse_args()))
