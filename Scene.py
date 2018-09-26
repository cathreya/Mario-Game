import assets
import random
import os
import SceneObject
from threading import Thread
import People
from time import sleep
import Blocks


class Scene:

    def __init__(self, player, score, sound):
        self.sound = sound
        sound.play("theme")
        self.score = score
        self.canGenerate = True
        self._progress = 0
        self._backGroundGraphics = [(assets.cloud, False), (assets.tree, True), (assets.clouds, False), (assets.mountain, False)]
        self._objectList = []
        self.ySize = 25
        self.xSize = 100
        self._bottom = [Blocks.Base(i, self.ySize) for i in range(self.xSize)]
        self.player = player
        self._personList = []
        self._personList.append(player)
        self.scene = [[" " for i in range(self.xSize)] for i in range (self.ySize)]
        self.over = False
        self.bg = [[" " for i in range(self.xSize)] for i in range(self.ySize + 5)]
        self.cur_bg = 0
        self.draw_bg(False, assets.cloud)
        self.boss = None

    def draw_bg(self, bot, asset):
        self.bg = [[" " for i in range(self.xSize)] for i in range(self.ySize + 5)]
        x = 0
        y = 0
        if bot:
            y = self.ySize - len(asset)
            x = self.xSize - len(asset[0])

        for i in range(len(asset)):
            for j in range(len(asset[i])):
                self.bg[y+i][x+j] = asset[i][j]

    def _generate(self):
        if self.canGenerate:
            num = random.randint(1, 50)
            y = random.randint(8, self.ySize-5)
            if 1 <= num <= 10:
                # generate a brick
                self._objectList.append(Blocks.Brick(self.xSize - 2, y, assets.brickBlock))
            elif num == 11:
                # generate a powerup block
                self._objectList.append(Blocks.Power(self.xSize - 2, y, assets.powerBlock))
            elif 12 <= num <= 22:
                # generate a coin
                self._objectList.append(Blocks.Coin(self.xSize - 2, y, assets.coinBlock))
            elif 23 <= num <= 33:
                # generate a hole
                for i in range(self.xSize-random.randint(4,8), self.xSize):
                    self._bottom[i] = Blocks.Hole(i, self.ySize, assets.Hole)
            elif 34 <= num <= 40:
                # generate a goomba
                self._personList.append(People.Enemy(self.xSize - 2, self.ySize - 2, (assets.goomba, assets.goomba, assets.goomba, assets.goomba), self.score.getLevel(), self.score.getLevel()*2))
            elif 41 <= num <= 50:
                # generate a spring
                self._objectList.append(Blocks.Spring(self.xSize - 2, y, assets.springBlock))

    def forward(self):
        player = self.player
        player.sprite = player.front_sprite

        player.move = 1 - player.move
        flag = 0
        can_move = player.speed
        init_x = player.x
        for i in range(player.speed+1):
            player.x += 1
            for obj in self._objectList:
                if obj.is_blocking() == 1 and obj.collision(player) == 1:
                    self.sound.play("bump")
                    flag = 1
                    break
            if flag == 1:
                can_move = i-1
                break
        player.x = init_x

        for obj in self._objectList:
            obj.x -= can_move
            if obj.x <= 2:
                self._objectList.remove(obj)

        for tile in self._bottom:
            tile.x -= can_move

        for i in range(can_move):
            self._bottom.pop(0)
            self._bottom.append(Blocks.Base(self.xSize-1, self.ySize))
            self._progress += 1
            if self._progress % 4 == 0:
                self._generate()

        if can_move == 0:
            return
        for i in range(self.ySize):
            beg = self.bg[i][0]
            for j in range(self.xSize - 1):
                self.bg[i][j] = self.bg[i][j + 1]
            self.bg[i][self.xSize - 1] = beg

    def backward(self):
        player = self.player
        player.sprite = player.back_sprite
        player.move = 1 - player.move
        flag = 0
        can_move = player.speed
        init_x = player.x

        for i in range(player.speed + 1):
            player.x -= 1
            for obj in self._objectList:
                if obj.is_blocking() == 1 and obj.collision(player) == 3:
                    self.sound.play("bump")
                    flag = 1
                    break
            if flag == 1:
                can_move = i - 1
                break
        player.x = init_x

        for obj in self._objectList:
            obj.x += can_move

        for tile in self._bottom:
            tile.x += can_move

        for i in range(can_move):
            self._bottom.pop(self.xSize - 1)
            self._bottom.insert(0, Blocks.Base(0, self.ySize))
            self._progress -= 1

        if can_move == 0:
            return
        for i in range(self.ySize):
            beg = self.bg[i][self.xSize-1]
            for j in range(self.xSize-1, 0, -1):
                self.bg[i][j] = self.bg[i][j-1]
            self.bg[i][0] = beg

    def jump(self, person):
        if not person.isJump:
            if person == self.player:
                self.sound.play("jump")
            person.sprite = person.jump_sprite
            for i in range(person.jumpHeight+1):
                person.y -= 1
                flag = 0
                for obj in self._objectList:
                    if obj.is_blocking() == 1 and obj.collision(person) == 4:
                        self.sound.play("bump")
                        flag = 1
                        break
                if flag == 1:
                    break

            person.isJump = True

    def write_to_scene(self, asset):
        self.scene = [j.copy() for j in self.bg]
        tmpdy = len(asset) // 2
        tmpdx = len(asset[0]) // 2

        starty = self.ySize // 2 - tmpdy
        startx = self.xSize // 2 - tmpdx

        for i in range(len(asset)):
            for j in range(len(asset[i])):
                self.scene[i + starty][j + startx] = asset[i][j]
        self.draw()
        # sleep(3)

    def reset_scene(self):
        self.sound.play("theme")
        self._bottom = [Blocks.Base(i, self.ySize) for i in range(self.xSize)]
        self._personList = [self.player]
        if self.boss is not None:
            self._personList.append(self.boss)
        self.player.y = int(self.ySize // 2)
        self.place()

    def level_up(self):
        self.sound.stop_sounds()
        self._progress = 0
        self.cur_bg = (self.cur_bg + 1) % len(self._backGroundGraphics)
        self.draw_bg(self._backGroundGraphics[self.cur_bg][1], self._backGroundGraphics[self.cur_bg][0])
        self.score.level_up()
        self.write_to_scene(assets.level)
        self.sound.play("level", block=True)
        self.canGenerate = True
        self.player.x = self.xSize//2
        self.reset_scene()

    def lost_life(self):
        self.sound.stop_sounds()
        dead = self.score.dead()
        if not dead:
            self.write_to_scene(assets.lost_life)
            self.sound.play("dead", block=True)
            self.reset_scene()
        else:
            self.over = True

    def game_over(self):
        self.sound.stop_sounds()
        self.write_to_scene(assets.game_over)
        self.sound.play("over", block=True)

    def gravity(self):
        for person in self._personList:
            person.y += 1
            flag = 0

            for obj in self._objectList:
                if obj.collision(person) == 2:
                    if obj.is_blocking() == 1:
                        flag = 1
                        break
                    elif obj.is_blocking() == 3:
                        flag = 2

            tile = self._bottom[person.x]

            if tile.is_blocking() == 1 and tile.collision(person) == 2:
                flag = 1

            if flag == 1:
                person.y -= 1
                person.isJump = False

            elif flag == 2:
                person.isJump = False
                self.jump(self.player)

            if person.y > self.ySize:
                if person == self.player:
                    self.lost_life()
                else:
                    self._personList.remove(person)
                    return

    def person_move(self):
        for person in self._personList:
            if person == self.player or person == self.boss:
                continue

            person.move = 1 - person.move
            flag = 0
            can_move = person.speed
            init_x = person.x

            for i in range(person.speed + 1):
                person.x -= 1
                for obj in self._objectList:
                    if obj.is_blocking() == 1 and obj.collision(person) == 3:
                        flag = 1
                        break
                if flag == 1:
                    can_move = i - 1
                    break

            person.x -= can_move
            k = random.randint(1,5)
            if k == 1 and not person.isProjectile:
                self.jump(person)

            k = int(person.collision(self.player))
            # tmp = ["no collision", "Left", "Top", "Right", "Bot"]
            # print(tmp[k], end="\r\n")
            if k == 2:
                self.sound.play("kill")
                self._personList.remove(person)
                self.score.enemy_kill()
                self.player.isJump = False
                self.jump(self.player)
            elif k != 0:
                self.lost_life()

            if person.x <= 2:
                self._personList.remove(person)

    def place(self):
        self.scene = [j.copy() for j in self.bg]
        player = self.player
        for obj in self._objectList:
            direction = int(obj.collision(player))
            # tmp = ["no collision", "Left", "Top", "Right", "Bot"]
            # print(tmp[direction], end="\r\n")

            if direction != 0 and obj.is_blocking() == 0:
                self.sound.play("coin")
                self.score.update_bonus(obj.getBonus())
                self._objectList.remove(obj)
                continue

            if obj.y - obj.dy < 0 or obj.y + obj.dy > self.ySize:
                continue
            elif obj.x - obj.dx < 0 or obj.x + obj.dx >= self.xSize:
                continue

            for i in range(len(obj.sprite[0])):
                for j in range(len(obj.sprite[0][i])):
                    self.scene[int(obj.y - obj.dy + i)][int(obj.x - obj.dx + j)] = obj.sprite[0][i][j]

        for person in self._personList:
            if person.y - 1 < 0 or person.y + 1 > self.ySize:
                continue
            elif person.x - 1 < 0 or person.x + 1 > self.xSize:
                continue
            for i in range(len(person.sprite[person.move])):
                for j in range(len(person.sprite[person.move][i])):
                    self.scene[person.y - person.dy + i][person.x - person.dx + j] = person.sprite[person.move][i][j]
        self.draw()

    def draw(self):
        os.system("tput cup 0 0")
        for i in range(self.ySize):
            for j in self.scene[i]:
                print(j, end="")
            print(end="\r\n")
        for i in self._bottom:
            print(i, end="")
        print(end="\r\n")
        print(self.score, end="\r\n")

    def boss_battle(self):
        if self._progress >= 1000 and self.boss is None:
            self._objectList = []
            self.canGenerate = False
            self.boss = People.Boss(self.xSize-4, self.ySize-4, (assets.boss, assets.boss, assets.boss, assets.boss), self.score.getLevel())
            self._personList.append(self.boss)

    def boss_move(self):
        if self.boss is not None:
            self.boss.move = 1 - self.boss.move

            if self.boss.x < self.player.x and self.boss.x < self.xSize-4:
                self.boss.x += self.boss.speed
            else:
                self.boss.x -= self.boss.speed

            k = random.randint(1, 5)
            if k == 1:
                self.jump(self.boss)
            if k == 4:
                self._personList.append(self.boss.shoot())

            k = int(self.boss.collision(self.player))
            if k == 2:
                self.sound.play("kill")
                dead = self.boss.dead()
                self.player.isJump = False
                self.jump(self.player)
                if dead:
                    self._personList.remove(self.boss)
                    self.boss = None
                    self.level_up()

            elif k != 0:
                self.lost_life()




class SceneThread(Thread):
    def __init__(self, event, scene):
        Thread.__init__(self)
        self.stopped = event
        self.scene = scene

    def run(self):
        while not self.stopped.wait(0.1):
            self.scene.boss_battle()
            self.scene.boss_move()
            self.scene.person_move()
            self.scene.gravity()
            self.scene.place()
