import argparse
import sys

from hitori import hitori_parser as hp
from hitori import hitori_solver as hs


argparser = argparse.ArgumentParser(
    description="Solves your Hitori puzzle for you!")

argparser.add_argument("filename", metavar="PATH", type=str,
                       help="path to your Hitori puzzle, in .txt format")

argparser.add_argument("-d", "--diagonal", action="store_true",
                       help="enables the additional diagonal rule "
                       "(no black diagonal repeats)")


def log_error(message):
    print(f"<HS_ERROR> {message}")


def main(argv=None):
    args = argparser.parse_args(argv)

    parser = hp.HitoriParser()
    try:
        board = parser.parse_board_from_file(args.filename)
        board.diagonal_rule_enabled = args.diagonal
    except FileNotFoundError as e:
        log_error(f"Could not locate the .txt file at \"{args.filename}\"")
        sys.exit(1)
    except ValueError as e:
        log_error(f"Invalid .txt file provided")
        sys.exit(2)

    solver = hs.HitoriSolver()
    try:
        solver.solve(board)
    except hs.HitoriNoSolutionError as e:
        log_error(f"Could not find a solution to this puzzle")
        sys.exit(3)

    print("Here is a solution:")
    print(board)
    sys.exit(0)


if __name__ == "__main__":
    main()
