import random
from typing import List

from casino.exceptions import DeckException
from casino.player import Player


class Table:
    def __init__(self, players_num: int) -> None:
        """
        Initialize new table
        :param players_num: number of poker players
        """
        self._deck = None
        self.players_num = players_num
        self.players = [Player(number=player_num) for player_num in range(1, players_num + 1)]
        self._community_hand = ""

    def generate_deck(self, deck_type: str) -> None:
        """
        Generate shuffled deck for game
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
        self._deck = [v + s for v in vals for s in suits]
        random.shuffle(self._deck)

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

    def deal_players(self) -> None:
        """
        Deal cards to players
        :return:
        """
        for player in self.players:
            player.add_hand(self.generate_hand(self._deck, hand_size=5))

    def deal_community(self) -> None:
        """
        Deal community cards
        :return:
        """
        self._community_hand += self.generate_hand(self._deck, hand_size=5)

    def flush_game(self):
        """
        Clean table
        :return:
        """
        self._community_hand = ""

    # def add_to_community(self, game_stage: str) -> None:
    #     """
    #     Add cards to community
    #     :param game_stage: Current game stage (flop, turn or river)
    #     :return: extended community cards
    #     """
    #     self.community_hand += self.generate_hand(self.deck, self.game_stages[game_stage])

    # def new_round(self) -> None:
    #     """
    #     Trigger new round of game (draw cards to community)
    #     :return:
    #     """
    #     self.current_game_stage = next(self.game_stages_iter)
    #     self.add_to_community(self.current_game_stage)

    @property
    def players_hands(self) -> str:
        """
        Show all players' hands
        :return: current players' hands
        """
        situation = ""
        for player in self.players:
            situation += "Player {} hand: {} \n".format(player.number, player.hand)
        return situation

    @property
    def hands(self) -> List[str]:
        return [player.hand for player in self.players]

    @property
    def game_cards(self):
        return self._community_hand + " " + " ".join([player.hand for player in self.players])

    @property
    def community_hand(self) -> str:
        """
        Show community cards
        :return: community cards on current stage
        """
        return self._community_hand

    @property
    def deck_size(self) -> int:
        return len(self._deck)
