import argparse
from sys import stdout

from hitori_board import HitoriBoard
from hitori_parser import HitoriParser
from hitori_solver import HitoriSolver, NoSolutionError


parser = argparse.ArgumentParser(
    description="Solves your Hitori puzzle for you!")

parser.add_argument("filename", metavar="PATH", type=str,
                    help="path to your Hitori puzzle, in .txt format")


def log_error(message):
    stdout.write(f"<Error> {message}")


def main():
    args = parser.parse_args()

    parser = HitoriParser()
    try:
        board = parser.parse_board_from_file(args.filename)
    except FileNotFoundError as e:
        log_error(f"{e}: Could not locate the .txt file")
        return

    solver = HitoriSolver()
    try:
        solved_board = solver.solve(board)
    except NoSolutionError as e:
        log_error(f"{e}: Could not find a solution to this puzzle")
        return

    stdout.write("Here is a solution:\n")
    stdout.write(solved_board)


if __name__ == "__main__":
    main()
