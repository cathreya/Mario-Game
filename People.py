import SceneObject
import assets


class Person(SceneObject.SceneObject):

    def __init__(self, x, y, sprite=("", "", "", ""), speed=2):
        SceneObject.SceneObject.__init__(self, x, y, sprite[0])
        self.front_sprite = sprite[1]
        self.back_sprite = sprite[2]
        self.jump_sprite = sprite[3]
        self.speed = speed
        self.jumpHeight = 8
        self.isJump = False
        self.move = 0

    def left(self):
        self.x -= self.speed
        self.sprite = self.back_sprite
        self.move = 1 - self.move

    def right(self):
        self.x += self.speed
        self.sprite = self.front_sprite
        self.move = 1 - self.move


class Enemy(SceneObject.SceneObject):

    def __init__(self, x, y, sprite=("", "", "", ""), speed=1, jumpHeight=4):
        SceneObject.SceneObject.__init__(self, x, y, sprite[0])
        self.front_sprite = sprite[1]
        self.back_sprite = sprite[2]
        self.jump_sprite = sprite[3]
        self.speed = speed
        self.jumpHeight = jumpHeight
        self.isJump = False
        self.move = 0

    def is_blocking(self):
        return 3


class Projectile(SceneObject.SceneObject):

    def __init__(self, x, y, sprite=("", "", "", ""), speed=1):
        SceneObject.SceneObject.__init__(self, x, y, sprite[0])
        self.front_sprite = sprite[1]
        self.back_sprite = sprite[2]
        self.jump_sprite = sprite[3]
        self.speed = speed
        self.move = 0
        self.isProjectile = True

    def is_blocking(self):
        return 0


class Boss(Enemy):

    def __init__(self, x, y, sprite=("", "", "", ""), level=1):
        speed = level + 1
        jumpHeight = level + 4
        Enemy.__init__(self, x, y, sprite, speed, jumpHeight)
        self.lives = level * 2

    def shoot(self):
        return Projectile(self.x, self.y, (assets.projectile, assets.projectile, assets.projectile, assets.projectile), self.lives//2+1)

    def dead(self):
        self.lives -= 1;
        if self.lives > 0:
            return False
        else:
            return True

    def is_blocking(self):
        return 3
