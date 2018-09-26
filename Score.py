from datetime import timedelta
import time
import random


class Score:

    def __init__(self):
        self.bonus_score = 0
        self.lives = 100
        self.start_time = time.time()
        self.coin_count = 0
        self._level = 1

    def update_bonus(self,bonus):
        self.bonus_score += bonus
        self.coin_count += 1

    def enemy_kill(self):
        b = random.randint(100, 500)
        self.bonus_score += b

    def level_up(self):
        self._level += 1
        self.bonus_score += 1000

    def getLevel(self):
        return self._level

    def dead(self):
        self.lives -= 1;
        if self.lives <= 0:
            self.lives = 0
            return True
        else:
            return False

    def __str__(self):
        cur_time = time.time()
        elapsed = cur_time - self.start_time
        score = int(self.bonus_score + elapsed)
        return "Level " + str(self._level) + " Lives: " + str(self.lives) + " Coins " + str(self.coin_count) + " Time: " + str(timedelta(seconds=elapsed))[:-7] + " Score: " + str(score)
