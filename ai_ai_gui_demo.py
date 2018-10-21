from goboard import GomokuGameHandler
from goboard.judge import Win, Lose
from goboard.logger import log
from ai.normal_ai import Ai as NormalAi
import time

black_player = NormalAi("black", board_size=(7, 7))
white_player = NormalAi("white", board_size=(7, 7))

try:
    with GomokuGameHandler(black_player, white_player, board_size=(7, 7)) as (black_round, white_round, board):
        for _ in range(11 * 11 // 2):
            black_round()
            time.sleep(0.3)
            white_round()
            time.sleep(0.3)

except Win as e:
    time.sleep(5)
    log('[end game] %s' % e)
except Lose as e:
    time.sleep(5)
    log('[end game] %s' % e)