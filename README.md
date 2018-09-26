# Python Terminal Mario

## Introduction

An infinite scrolling Mario-like platformer game written from scratch in Python. 

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
