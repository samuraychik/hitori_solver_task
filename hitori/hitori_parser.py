from hitori.hitori_board import HitoriBoard


class HitoriParser:
    def parse_board_from_file(self, filename: str) -> HitoriBoard:
        with open(filename, "r") as f:
            width, height = map(int, f.readline().strip().split())
            numbers = []
            for _ in range(height):
                row = map(int, f.readline().strip().split())
                numbers.extend(row)
            return HitoriBoard(width, height, numbers)

    def parse_file_from_board(self, path: str, board: HitoriBoard) -> None:
        with open(path, "w") as f:
            f.write(f"{board.width} {board.height}")
            for y in range(board.height):
                row = " ".join([str(n.value) for n in board.get_row(y)])
                f.write("\n")
                f.write(row)
