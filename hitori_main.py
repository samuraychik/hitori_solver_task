import argparse

from hitori_solver import hitori_parser
from hitori_solver import hitori_solver


argparser = argparse.ArgumentParser(
    description="Solves your Hitori puzzle for you!")

argparser.add_argument("filename", metavar="PATH", type=str,
                       help="path to your Hitori puzzle, in .txt format")


def log_error(message):
    print(f"<H_ERROR> {message}")


def main():
    args = argparser.parse_args()

    parser = hitori_parser.HitoriParser()
    try:
        board = parser.parse_board_from_file(args.filename)
    except FileNotFoundError as e:
        log_error(f"{e}: Could not locate the .txt file")
        return

    solver = hitori_solver.HitoriSolver()
    try:
        solver.solve(board)
    except hitori_solver.HitoriNoSolutionError as e:
        log_error(f"{e}: Could not find a solution to this puzzle")
        print(board)
        return

    print("Here is a solution:")
    print(board)


if __name__ == "__main__":
    main()
