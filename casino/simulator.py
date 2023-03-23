from textwrap import wrap
from typing import List

from casino.table import Table
from evaluator.evaluator import Evaluator


class Simulator:
    def __init__(self, players_num: int = 3, simulations_num: int = 10000):
        """

        :param players_num: number of players
        :param simulations_num: number of simulations
        """
        self._simulations_num = simulations_num
        self.table = Table(players_num=players_num)
        self.evaluator = Evaluator()

    def simulate(self, deck_type: str = "full"):
        """
        Simulates a number of poker games
        :param deck_type: number of cards in deck (52 for full, 36 for short)
        :return:
        """
        for i in range(self._simulations_num):
            self.table.generate_deck(deck_type)
            self.table.set_stage_deck(self.table.hands)
            self.table.set_stage_deck(self.table.start_community_hand)
            self.table._community_hand = self.table.start_community_hand
            rounds = self.table.set_stage_iterator(self.table.start_game_stage)
            for round_num in range(rounds):
                self.table.new_round()
            print(f"Community hand: {self.table.community_hand}")
            hands, ranks = self.play(self.table.community_hand, self.table.hands)
            for player in self.table.players:
                if player.hand == hands[0]:
                    player.wins_game()
            self.table.flush_game()

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

    def show_status(self) -> None:
        """
        Show win probability from all simulations
        :return:
        """
        for player in self.table.players:
            print("Player {} with {:.2f} percent win probability".format(player.number, player.wins / 100))
