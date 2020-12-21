from textwrap import wrap
from evaluator.evaluator import *
import re

GAMES = ['texas-holdem',
         'omaha-holdem',
         'five-card-draw'
         ]

LENGTH_MAP = {
    'texas-holdem': [5, 2, 4],
    'omaha-holdem': [5, 4, 8],
    'five-card-draw': [5, 5, 10]
}


def validate_hands(game_type, hands):
    for i in hands:
        if len(i) != LENGTH_MAP[game_type][2]:
            return False
    return True


def validate_input(string):
    ret = True
    pattern = re.compile("[AKQJT2-9][hdcs]")
    res = pattern.findall(string)
    if res is None or len(res) < len(string) // 2:
        ret = False
    return ret


def validate_unique(cards_list):
    return False if len(set(cards_list)) < len(cards_list) else True


def validate_length(game_type, cards_list):
    ret = True
    if len(cards_list[:5]) % LENGTH_MAP[game_type][0] and len(cards_list[5:]) % LENGTH_MAP[game_type][1]:
        ret = False
    return ret


def validate_game(args):
    ret, message = True, 'OK'
    curr_game = list(wrap(args['board'], 2) + list(wrap(''.join(args['hands']), 2)))
    if (args['game_type']) not in GAMES:
        ret, message = False, 'Error: Unknown type of poker game'
    elif not (validate_input(args['board'] + ''.join(args['hands']))):
        ret, message = False, 'Error: Invalid cards input'
    elif not validate_hands(args['game_type'], args['hands']):
        ret, message = False, 'Error: Invalid hand length'
    elif not (validate_unique(curr_game)):
        ret, message = False, 'Error: Cards are not unique'
    elif not (validate_length(args['game_type'], curr_game)):
        ret, message = False, 'Error: Not enough cards to evaluate hands'
    return ret, message


def cards_pretty_print(hands, ranks):
    size = len(ranks)
    string = ''
    for i in range(size - 1):
        string += ''.join(hands[i])
        if ranks[i] == ranks[i + 1]:
            string += '='
        else:
            string += ' '
    string += ''.join(hands[-1])
    print(string)


def play(args):
    evaluator = Evaluator()
    args['board'] = tuple(wrap(args['board'], 2))
    hands = list(map(lambda x: tuple(wrap(x, 2)), args['hands']))
    if args['game_type'] == 'five-card-draw':
        hands.append(args['board'])
        ranks = list(map(lambda x: evaluator.evaluate_cards(*x), hands))
        hands.sort(key=lambda x: evaluator.evaluate_cards(*x), reverse=True)
    else:
        hands.sort(key=lambda x: evaluator.evaluate_cards(*args['board'], *x), reverse=True)
        ranks = list(map(lambda x: evaluator.evaluate_cards(*args['board'], *x), hands))
    cards_pretty_print(hands, ranks)
