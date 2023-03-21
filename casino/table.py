import random
from typing import List

from casino.exceptions import DeckException


class Table:
    def __init__(self, players_num: int, hand_size: int, deck_type: str):
        self.deck = self.generate_deck(deck_type)
        self.players_num = players_num
        self._player_hands = {
            player_num: self.generate_hand(self.deck, hand_size) for player_num in range(1, players_num + 1)
        }
        self._community_hand = ""
        self.game_stages = {
            "flop": 3,
            "turn": 1,
            "river": 1
        }
        self.current_game_stage = "preflop"

    @staticmethod
    def generate_deck(deck_type: str) -> List[str]:
        """
        Generate deck for game
        :param deck_type: type of deck: full of short
        :return: deck (list of strings)
        """
        if deck_type == "full":
            vals = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        elif deck_type == "short":
            vals = ["6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        else:
            raise DeckException("Invalid Deck Type. Valid options are: full/short ")

        suits = ["s", "c", "h", "d"]
        deck = [v + s for v in vals for s in suits]
        random.shuffle(deck)
        return deck

    def generate_hand(self, deck: List[str], hand_size: int = 4) -> str:
        """
        Generate hand (for player or community)
        :param deck: deck of cards
        :param hand_size: number of cards to give
        :return: hand
        """
        hand = ""
        if hand_size < len(deck):
            for i in range(hand_size):
                hand += deck[0]
                deck.pop(0)
        return hand

    def add_to_community(self, game_stage: str) -> None:
        """
        Add cards to community
        :param game_stage: Current game stage (flop, turn or river)
        :return: extended community cards
        """
        self._community_hand += self.generate_hand(self.deck, self.game_stages[game_stage])

    def new_round(self):
        self.current_game_stage =

    @property
    def players_hands(self):
        situation = ""
        for k, v in self._player_hands.items():
            situation += "Player {} hand: {} \n".format(k, v)
        return situation

    @property
    def community_hand(self):
        return self._community_hand

    @property
    def deck_size(self):
        return len(self.deck)

