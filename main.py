import Scene
import os
import tty
import sys
import termios
from threading import Event
import People
import assets
import Score
import Sound


def main():

    sound = Sound.Sound()
    score = Score.Score()
    player = People.Person(0, 0, (assets.mario, assets.mario, assets.mario_back, assets.mario_jump), speed=2)
    scene = Scene.Scene(player, score, sound)

    player.x = int(scene.xSize / 2)
    player.y = int(scene.ySize - 2)

    # Backing up original attributes
    orig_settings = termios.tcgetattr(sys.stdin)
    # Setting up stdin in raw mode
    tty.setraw(sys.stdin)
    os.system("setterm -cursor off")

    # Starting the scene thread
    stopFlag = Event()
    timerThread = Scene.SceneThread(stopFlag, scene)
    timerThread.start()

    scene.place()
    k = 'o'

    while k != "q" and not scene.over:
        k = sys.stdin.read(1)[0]
        if k == "d":
            if scene.boss is None:
                scene.forward()
            else:
                player.right()
        elif k == "a":
            if scene.boss is None:
                scene.backward()
            else:
                player.left()
        elif k == "w":
            scene.jump(player)

    # Ending the scene thread
    stopFlag.set()
    # Drawing the game over screen
    scene.game_over()
    sound.stop_sounds()
    # Restoring Terminal to original settings
    os.system("setterm -cursor on")
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)


if __name__ == '__main__':
    main()