import argparse
import sys

from hitori import hitori_generator as hg
from hitori import hitori_parser as hp


argparser = argparse.ArgumentParser(
    description="Solves your Hitori puzzle for you!")

argparser.add_argument("path", metavar="PATH", type=str,
                       help="generated file path")
argparser.add_argument("width", metavar="W", type=int,
                       help="puzzle width (must be positive)",
                       default=5)
argparser.add_argument("height", metavar="H", type=int,
                       help="puzzle height (must be positive)",
                       default=5)
argparser.add_argument("-d", "--diagonal", action="store_true",
                       help="enables the additional diagonal rule "
                       "(no black diagonal repeats)")


def log_error(message):
    print(f"<HG_ERROR> {message}")


def main(argv=None):
    args = argparser.parse_args(argv)

    if args.width < 0:
        log_error(f"Invalid width {args.width} (must be positive)")
        sys.exit(1)
    if args.height < 0:
        log_error(f"Invalid height {args.height} (must be positive)")
        sys.exit(1)

    geneartor = hg.HitoriGenerator()
    generated = False
    fails = 0
    while not generated:
        if fails > 42:
            log_error("Failed to generate a puzzle :(")
            sys.exit(2)
        try:
            board = geneartor.generate(args.width, args.height, args.diagonal)
        except hg.HitoriRetryGenerationError:
            fails += 1
        else:
            generated = True

    parser = hp.HitoriParser()
    try:
        parser.parse_file_from_board(args.path, board)
    except FileNotFoundError:
        log_error(f"Couldn't reach the path \"{args.path}\"")
        sys.exit(3)

    print(f"Board generated at \"{args.path}\" successfully!")
    print(board)
    sys.exit(0)


if __name__ == "__main__":
    main()
