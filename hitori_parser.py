from hitori_board import HitoriBoard


class HitoriParser:
    def parse_board_from_file(self, filename: str) -> HitoriBoard:
        with open(filename) as f:
            size = int(f.readline().strip())
            numbers = []
            for _ in range(size):
                row = map(int, f.readline().strip().split())
                numbers.extend(row)
            return HitoriBoard(size, numbers)
