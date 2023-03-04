class MoveMatrix:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.inner = [[True for _ in range(width)] for _ in range(height)]

    def get(self, x: int, y: int):
        if x not in range(self.width) or y not in range(self.height):
            return False  # walls are automatically not valid
        return self.inner[y][x]

    def set(self, x: int, y: int, value: bool):
        self.inner[y][x] = value
