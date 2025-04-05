Zombie Survival Game
AI vs AI Zombie Survival Game

Description:-
  This is an AI vs AI simulation game where autonomous humans try to survive against a growing zombie horde. The game features:
  Human AI with pathfinding, fear-based decision making, and combat behaviors
  Zombie AI that chases humans using pathfinding and has varying aggression levels
  A Pathfinding* for both humans and zombies to navigate around obstacles
  Dynamic spawning system that increases the zombie threat over time
  Time-based survival mode where humans must last 60 seconds to win

Features:-
  Autonomous Agents: Both humans and zombies make their own decisions based on game state
  Obstacle Avoidance: Uses grid-based pathfinding to navigate complex environments
  Combat System: Humans can shoot at zombies with limited ammo and reload times
  Visual Feedback: Blood splatters, health bars, and directional sprites
  Game Mechanics: Fear system, safe zones, zombie conversion, and time-based victory

Requirements:-
  Python 3.x
  Pygame library

Installation:-
  Clone the repository:-
    git clone https://github.com/Maruthi5760/maruthi
    cd ai-zombie-survival
  Install the required dependencies:
    pip install pygame
  Run the game:-
  python zom_surv.py
Controls:-
  ESC: Quit the game
  R: Restart after game over

Game Rules:-
  Humans win if at least one survives for 60 seconds
  Zombies win if all humans are converted to zombies

Humans will:
  Seek safe zones when scared
  Shoot at nearby zombies
  Flee when zombies get too close
Zombies will:
  Chase the nearest human
  Become more aggressive when close to prey
  Convert humans they catch

Customization:-
  You can modify these constants in the code:
  WIDTH, HEIGHT: Screen dimensions
  FPS: Game speed
  BULLET_SPEED, ZOMBIE_SPEED, HUMAN_SPEED: Movement speeds
  SPAWN_RATE: How often new zombies appear
  GAME_DURATION: Survival time needed to win

Future Improvements:-
  Add different human/zombie types with varied abilities
  Implement weapons/items humans can find
  Add sound effects and music
  Create more complex maps with choke points
  Add difficulty settings

Credits:-
Created using Python and Pygame. in assets,we have given the png files of required images if images can't be loaded we can have used pygame to draw human and zombies and background

Enjoy watching the AI battle it out!
