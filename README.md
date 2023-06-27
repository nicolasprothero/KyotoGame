# Game Name: Weaponize

## Description
Weaponize is a 2D platform/combat game that allows two players to duel against each other. The gameplay revolves around multiple short combat rounds with quick and precise movement. After the preliminary rounds, players will be given a randomized weapon based on their performance. The game will feature a variety of weapons with unique characteristics, such as range, damage, and attack speed, etc. The game will also feature a random case opening system to obtain various weapons. The game is developed using the Pygame library and is currently under development.

## Gameplay
1. Spawning: The game begins by spawning the two players on opposite sides of the map.
2. Controls: Each player has control over their character, equipped with a weapon and a dash ability. The controls will be customizable and detailed in the game's options menu.
3. Movement: Players can move left and right on the platforms and jump between platforms, using strategy to gain an advantage.
4. Weapons: Each player starts with a default weapon. More weapons will be obtained through the random case opening system. Different weapons will have unique characteristics, such as range, damage, and attack speed, etc.
5. Combat: Players can attack by swinging their weapon at their opponent. The objective is to hit the other player before they hit you.
6. Lives and Damaged State: Each player has one life per round. When a player is hit, they become damaged for a set time. While in this state, the player can be eliminated by their opponent if they land a successful hit.
7. Dash Ability: Players have a dash ability that allows them to quickly evade attacks or close the distance between them and their opponent. 
8. Game End: As of now, the game ends when a player is hit by their opponent while in the damaged state. The players are then prompted with the option to play again or return to the menu.


## Installation and Setup Instructions

### Creating the distribution package
python setup.py sdist


### 1. Install the package
pip install ./Weaponize-1.0.tar.gz

### 2. Run the game
weaponize


## Github Link
https://github.com/nicolasprothero/KyotoGame