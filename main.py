from evaluator.utils import *
import sys


if __name__ == "__main__":
    args = {}
    for line in sys.stdin:
        tmp = line.strip().split()
        args['game_type'] = tmp[0]
        args['board'] = tmp[1]
        args['hands'] = tmp[2:]
        ret, message = validate_game(args)
        if ret:
            play(args)
        else:
            print(message)
