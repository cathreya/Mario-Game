import assets
import random


class SceneObject:

    def __init__(self, x, y, sprite=""):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.dx = len(self.sprite[0][0]) // 2
        self.dy = len(self.sprite[0]) // 2
        self.isProjectile = False

    def collision(self, player):
        x1 = self.x - self.dx
        x2 = self.x + self.dx
        y1 = self.y - self.dy
        y2 = self.y + self.dy

        px1 = player.x - player.dx
        px2 = player.x + player.dx
        py1 = player.y - player.dy
        py2 = player.y + player.dy

        if x1 <= px2 and x2 >= px1 and y1 <= py2 and y2 >= py1:
            return self.collision_direction(player)
        else:
            return 0

    # 1 Left 2 Top 3 Right 4 Bot
    def collision_direction(self, player):
        playerBot = player.y + player.dy
        myBot = self.y + self.dy
        playerRight = player.x + player.dx
        myRight = self.x + self.dx

        bCollision = myBot - player.y
        tCollision = playerBot - self.y
        lCollision = playerRight - self.x
        rCollision = myRight - player.x

        if tCollision <= min(bCollision, lCollision, rCollision):
            # Top Collision
            return 2
        elif bCollision <= min(tCollision, lCollision, rCollision):
            # Bot Collision
            return 4
        elif lCollision <= min(tCollision, bCollision, rCollision):
            # Left Collision
            return 1
        elif rCollision <= min(tCollision, bCollision, lCollision):
            # Right Collision
            return 3

        return 0

    def is_blocking(self):
        pass
