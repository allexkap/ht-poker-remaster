class Player:
    def __init__(self, number: int,  hand: str):
        self.number = number
        self._hand = hand
        self._wins = 0

    @property
    def hand(self):
        return self._hand

    def wins_game(self):
        self._wins += 1

    def __str__(self):
        return "Player {} with {} wins".format(self.number, self._wins)
