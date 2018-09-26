# Python Terminal Mario

## Introduction

An infinite scrolling Mario-like platformer game written in Python. 

## OO Structure

- **Inheritance**: A generic `SceneObject` class from which various Blocks, Enemy and Player classes are derived.

- **Encapsulation**: All attributes and methods of an object are bundled into a single unit. The `Scene` class contains all the essential functionalities to run the game.

- **Polymorphism**: Overloads the `__str__()` to make printing easier. Certain methods and attributes are overriden in child classes.

- **Abstraction**: Implementation details are hidden from the user. Users can construct and modify the game using the scene and player methods.

## Controls

- `W` - Jump
- `A` - Left
- `D` - Right

## Gameplay

- Blocks randomly spawn on screen:-
	- Brick Block: Cannot be destroyed or crossed
	- Spring Block: Can be crossed, causes a bounce on landing
	- Coins: Gain bonus score by collecting these

- Levels:-
	- Player needs to cross a certain distance to complete a level
	- In order to progress to the next level a boss must be defeated
	- Each level presents a different scenery (clear sky, trees, cloudy sky, mountains) and a higher difficulty level

- Enemies:-
	- Enemies spawn randomly and move and jump based on the current level. Higher the level faster the enemies and higher their jumps.
	- Touching an enemy causes you to lose a life, however enemies can be killed by stomping them from the top (directional collision)

- Bosses:-
	- Bosses are special enemies with several lives depending on the level.
	- Bosses are able to fire projectiles at the player. Touching a projectiles causes tou to lose a life.
	- Bosses also show intelligent targeting based on the player's location.

- Score:-
	- Scoring is based on how long the player can survive.
	- Bonus score is awarded for collecting coins, killing enemies and clearing levels.

- Sound Effects:-
	- The Sound class accesses wav files present in the Media directory.
	- Sound depends on `play` which requires the `sox` package in Linux.

## Running the program

- Install the requirements:
	- `pip3 install -r requirements.txt`
- Run the program using
	- `python3 main.py`


## File Structure

```
├── assets.py
├── Blocks.py
├── __init__.py
├── main.py
├── Media
│   ├── 01-main-theme-overworld.mp3
│   ├── 01-main-theme-overworld.wav
│   ├── smb_breakblock.wav
│   ├── smb_bump.wav
│   ├── smb_coin.wav
│   ├── smb_gameover.wav
│   ├── smb_jump-small.wav
│   ├── smb_jump-super.wav
│   ├── smb_mariodie.wav
│   ├── smb_stage_clear.wav
│   └── smb_stomp.wav
├── People.py
├── README.md
├── requirements.txt
├── SceneObject.py
├── Scene.py
├── Score.py
└── Sound.py
```
