# Final---Zombies

![Zombies Demo](Zombie.mp4)

Zombies is a two-player game where the goal is to capture the golden orb that randomly moves around the playing area. When a player touches the orb, it relocates to another random location on the playing area and zombies are spawned. The number of zombies spawned increases by two each time the orb is touched. For example, the first touch spawns four zombies (two per player), the second touch spawns six zombies (three per player), the third touch spawns eight zombies(four per player), and so on. The zombies pursue the players around the playing area.

Players can defend themselves by shooting and removing the zombies from the game. Players can also drop bombs that destroy multiple zombies at once. If any zombie touches either player, the game ends and a message appears celebrating the winning player.


## Player Class:
- Will constantly move forward 5 pixels each time the display is updated.
- Will remain within the defined playing area. If the player touches the boundary, it will reflect off the boundary and continue moving forward.
- The user will use key presses to control the player: turn left, turn right, fire bullet, and drop bomb.
- A player object will be hidden ("die") when it collides with a Zombie object.
- Each player will:
    - Maintain a list of Bullet objects (rounds)
    - Maintain a list of Bomb objects (bombs)
- Dropping a bomb:
    - Each player will have a limit of 3 bombs for the entire game.
    - Decreases the bomb count
    - Creates a Bomb object at the player’s current location

## Prize Class:

- Will move randomly around the defined playing area.

- If the player touches the prize:
    - The prize will relocate to a random position in the playing area
    - Zombie objects will be instantiated at random locations in the playing area
    - Equal number of Zombie object will follow and attack player 1 and player 2
    - Number of zombies will increase by two each time the prize is touched

## Zombie Class:

- Objects of the Zombie class will continuously face the player using the towards() method.
    ``` python
    zombie.setheading(zombie.towards(p1))
    zombie.forward(2)
    ```

- Zombie objects will continuously move towards the player at 2 to 3 pixels per update.

- A zombie object will be instantiated (created) every time the player touches the prize.

- A Zombie object will be destroyed and removed from the list when it is hit by a Bullet object or destroyed by a Bomb.

## Bullet Class:

- Will originate at the location of the Player object which fired it.
- Each Bullet object will have the heading of the player object.
- Bullet objects will move in straight lines.
- Bullet objects will be destroyed if:
    - They collide with a zombie
    - They leave the playing area

## Bomb Class:

- Will originate at the location of the Player object that dropped it.
- Each Bomb object will:
    - Be placed at the player’s current position
    - Wait for a short delay (~1 second) before exploding

- When the bomb explodes:
    - A circular blast radius of approximately 100 pixels will be drawn
    - All Zombie objects within this radius will be destroyed and removed from the game

- After exploding:
    - The bomb will remove itself from the player’s bomb list
    - The explosion drawing will be cleared
