import argparse

from hitori_board import HitoriBoard
from hitori_parser import HitoriParser
from hitori_solver import HitoriSolver, HitoriNoSolutionError


argparser = argparse.ArgumentParser(
    description="Solves your Hitori puzzle for you!")

argparser.add_argument("filename", metavar="PATH", type=str,
                    help="path to your Hitori puzzle, in .txt format")


def log_error(message):
    print(f"<ERROR> {message}")


def main():
    args = argparser.parse_args()
    
    parser = HitoriParser()
    try:
        board = parser.parse_board_from_file(args.filename)
        # board = parser.parse_board_from_file(r"puzzles\1.txt")
    except FileNotFoundError as e:
        log_error(f"{e}: Could not locate the .txt file")
        return

    solver = HitoriSolver()
    try:
        solver.solve(board)
    except HitoriNoSolutionError as e:
        log_error(f"{e}: Could not find a solution to this puzzle")
        return

    print("Here is a solution:")
    print(board)


if __name__ == "__main__":
    main()
