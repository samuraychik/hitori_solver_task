import argparse
import sys
from hitori_parser import HitoriParser
# from ... import ...


parser = argparse.ArgumentParser(
    description="Solves your Hitori puzzle for you!")

parser.add_argument("filename", metavar="PATH", type=str,
                    help="path to your Hitori puzzle, in .txt format")


def log_error(message):
    sys.stdout.write(f"<Error> {message}")


def main():
    args = parser.parse_args()
    try:
        parsed = HitoriParser().parse_file(args.filename)
    except FileNotFoundError as e:
        log_error(f"{e}: Couldn't locate the .txt file")
    # ...


if __name__ == "__main__":
    main()
