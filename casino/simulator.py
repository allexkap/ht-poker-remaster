from textwrap import wrap
from typing import List

from casino.table import Table
from evaluator.evaluator import Evaluator


class Simulator:
    def __init__(self, players_num: int = 3, simulations_num: int = 100):
        self._simulations_num = simulations_num
        self._table = Table(players_num=players_num)
        self.evaluator = Evaluator()

    def simulate(self, deck_type: str = "full"):
        """
        Simulates a number of poker games
        :param players_num: number of players at table
        :param hand_size: max number of cards for player
        :param deck_type: number of cards in deck (52 for full, 36 for short)
        :return:
        """
        for i in range(self._simulations_num):
            self._table.generate_deck(deck_type)
            self._table.deal_players()
            self._table.deal_community()
            hands, ranks = self.play(self._table.community_hand, self._table.hands)
            for player in self._table.players:
                if player.hand == hands[0]:
                    player.wins_game()
            self._table.flush_game()

    def play(self, community_hand: str, players_hands: List[str]):
        """
        Simulates one poker game
        :param community_hand: cards on table
        :param players_hands: cards in players' pockets
        :return: all players' hands with appropriate ranks (the less the rank the better hand is)
        """
        board = tuple(wrap(community_hand, 2))
        hands = list(map(lambda x: tuple(wrap(x, 2)), players_hands))
        hands.sort(key=lambda x: self.evaluator.evaluate_cards(*board, *x))
        ranks = list(map(lambda x: self.evaluator.evaluate_cards(*board, *x), hands))
        hands = [''.join(hand) for hand in hands]
        return hands, ranks

    def show_status(self):
        """
        Show win probability from all simulations
        :return:
        """
        for player in self._table.players:
            print("Player {} with {} win probability".format(player.number, player.wins / self._simulations_num))
