from textwrap import wrap
import itertools as it
from multiprocessing import Pool

from casino.table import Table
from evaluator.evaluator import Evaluator



class Simulator:

    def __init__(self, players_num: int = 3, procces_num = 4):
        self.players_num = players_num
        self.procces_num = procces_num
        self.table = Table(players_num=players_num)
        self.evaluator = Evaluator()
        self.players_wins = [0] * players_num
        self.cache = None


    def simulate(self, deck_type: str = "full"):
        self.table.generate_deck(deck_type)
        self.table.set_stage_deck(self.table.hands)
        self.table.set_stage_deck(self.table.start_community_hand)

        players_hands = tuple(map(lambda x: tuple(wrap(x, 2)), self.table.hands))
        community_hand = tuple(wrap(self.table.start_community_hand, 2))

        comb_num = 5-len(self.table.start_community_hand)//2
        all_decks = tuple(it.combinations(self.table._deck, comb_num))
        n = self.procces_num
        part = len(all_decks)//n

        self.cache = (players_hands, community_hand)
        args = [all_decks[i*part:(i+1)*part] for i in range(n)]
        with Pool(n) as p:
            res = p.map(self.play_multiply, args)

        self.players_wins = [sum(res[i][j] for i in range(self.procces_num)) for j in range(self.players_num)]


    def play_multiply(self, deck_cards_set):
        players_hands, community_hand = self.cache
        players_wins = [0] * len(players_hands)
        for deck_cards in deck_cards_set:
            result = tuple(self.evaluator.evaluate_cards(*community_hand, *deck_cards, *player_hand) for player_hand in players_hands)
            winner_score = min(result)
            for i in range(len(result)):
                if result[i] == winner_score:
                    players_wins[i] += 1
        return players_wins


    def show_status(self):
        total = sum(self.players_wins)
        for player, player_wins in zip(self.table.players, self.players_wins):
            print("Player {} with {:.2f} percent win probability".format(player.number, player_wins / total * 100))
