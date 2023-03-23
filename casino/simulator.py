from itertools import combinations
from textwrap import wrap
from typing import List

from casino.table import Table
from evaluator.evaluator import Evaluator


class Simulator:
    def __init__(self, players_num: int = 3, simulations_num: int = 10):
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
        # for i in range(self._simulations_num):
        #     self.table.generate_deck(deck_type)
        #     self.table.set_stage_deck(self.table.hands)
        #     self.table.set_stage_deck(self.table.start_community_hand)
        #     self.table._community_hand = self.table.start_community_hand
        #     # rounds = self.table.set_stage_iterator(self.table.start_game_stage)
        #     # for round_num in range(rounds):
        #     #     self.table.new_round()
        #     all_combinations, s = self.table.get_all_deck_combinations()
        #     for combination in all_combinations:
        #         self.table._community_hand = self.table.start_community_hand + "".join(combination)
        #         hands, ranks = self.play(self.table.community_hand, self.table.hands)
        #         print(hands, ranks)
        #         for player in self.table.players:
        #             # if player.hand == hands[0]:
        #             if hands[0] in player.hand:
        #                 player.wins_game()
        #                 print(f"Player {player.number} wins")
        #     self.table.flush_game()
        all_combinations, all_combinations_num = self.table.get_all_deck_combinations()
        for combination in all_combinations:
            self.table._community_hand = self.table.start_community_hand + "".join(combination)
            hands, ranks = self.play(self.table.community_hand, self.table.hands)
            for player in self.table.players:
                if player.hand == hands[0]:
                    player.wins_game()
                    print(f"Player {player.number} wins")
        self._simulations_num = all_combinations_num

    def evaluate_one_player(self, board: tuple, hand: str):
        # print(board)
        all_4_combinations = [hand[2:], hand[:2] + hand[4:], hand[:4] + hand[6:], hand[:6] + hand[8:], hand[:8]]
        for i in range(len(all_4_combinations)):
            all_4_combinations[i] = tuple(wrap(all_4_combinations[i], 2))
        all_4_combinations.sort(key=lambda x: self.evaluator.evaluate_cards(*board, *x))
        ranks = list(map(lambda x: self.evaluator.evaluate_cards(*board, *x), all_4_combinations))
        print(all_4_combinations)
        print(ranks)
        return all_4_combinations[0], ranks[0]

    def play(self, community_hand: str, players_hands: List[str]):
        """
        Simulates one poker game
        :param community_hand: cards on table
        :param players_hands: cards in players' pockets
        :return: all players' hands with appropriate ranks (the less the rank the better hand is)
        """
        print(community_hand)
        board = tuple(wrap(community_hand, 2))
        hands = list(map(lambda x: tuple(wrap(x, 2)), players_hands))
        print(hands)
        highest_hands, highest_ranks = [], []
        for hand in players_hands:
            hand, rank = self.evaluate_one_player(board, hand)
            highest_hands.append(''.join(hand))
            highest_ranks.append(rank)
        print(highest_hands, highest_ranks)
        # hands_map = {
        #     ''.join(hand): highest_rank for hand in hands for highest_rank in highest_ranks
        # }
        cards_values = list(zip(highest_hands, highest_ranks))
        print(cards_values)
        # print(hands_map)
        # hands.sort(key=lambda x: self.evaluator.evaluate_cards(*board, *x))
        # ranks = list(map(lambda x: self.evaluator.evaluate_cards(*board, *x), hands))
        # hands = [''.join(hand) for hand in hands]
        # highest_hands = [''.join(highest_hand) for highest_hand in highest_hands]
        # print(highest_hands)
        # return highest_hands, highest_ranks
        # print(hands, ranks)
        # hands_map_sorted = {k: v for k, v in sorted(hands_map.items(), key=lambda item: item[1], reverse=True)}
        # print(hands_map_sorted)
        # hands, ranks = [hand for hand in hands_map_sorted.keys()], list(hands_map_sorted.values())
        return hands, ranks
    def show_status(self) -> None:
        """
        Show win probability from all simulations
        :return:
        """
        print(self._simulations_num)
        for player in self.table.players:
            print(player.wins)
            print("Player {} with {:.2f} percent win probability".format(
                player.number, player.wins / self._simulations_num
            )
        )
