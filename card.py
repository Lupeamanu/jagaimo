'''Card utility'''


class Card:
    def __init__(self, front: str, back: str) -> None:
        self.front: str = front
        self.back: str = back

        self.id: int = hash(f'{front + back}')
