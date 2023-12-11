from hitori_board import HitoriBoard


class HitoriParser:
    def parse_board_from_file(filename: str) -> HitoriBoard:
        with open(filename) as f:
            width, height = map(int, f.readline().strip().split())
            numbers = []
            for _ in range(height):
                row = map(int, f.readline().strip().split())
                numbers.extend(row)
            return HitoriBoard(width, height, numbers)
