from SceneObject import SceneObject
import random
import assets


class Coin(SceneObject):

    def __init__(self, x, y, sprite=assets.coinBlock):
        SceneObject.__init__(self, x, y, sprite)
        self._bonus = random.randint(1,10)

    def is_blocking(self):
        return 0

    def getBonus(self):
        return self._bonus


class Hole(SceneObject):

    def __init__(self, x, y, sprite=assets.Hole):
        SceneObject.__init__(self, x, y, sprite)

    def is_blocking(self):
        return -1

    def __str__(self):
        return self.sprite[0][0]


class Brick(SceneObject):

    def __init__(self, x, y, sprite=assets.brickBlock):
        SceneObject.__init__(self, x, y, sprite)
        self.canBreak = True

    def is_blocking(self):
        return 1


class Power(SceneObject):

    def __init__(self, x, y, sprite=assets.powerBlock):
        SceneObject.__init__(self, x, y, sprite)
        self.canBreak = True
        self.bonus = random.randint(1,10)

    def is_blocking(self):
        return 1


class Base(SceneObject):

    def __init__(self, x, y, sprite=assets.bottomTile):
        SceneObject.__init__(self, x, y, sprite)

    def is_blocking(self):
        return 1

    def __str__(self):
        return self.sprite[0][0]


class Spring(SceneObject):
    def __init__(self, x, y, sprite=assets.springBlock):
        SceneObject.__init__(self, x, y, sprite)

    def is_blocking(self):
        return 3

    def __str__(self):
        return self.sprite[0][0]
