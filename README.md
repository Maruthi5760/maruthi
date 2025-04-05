# 🧟‍♂️ AI vs AI Zombie Survival Game
!GAME_OVER["assests/game_screenshot"]
An **AI simulation** game where autonomous humans and zombies engage in a survival battle. Watch as smart humans try to survive against an evolving zombie horde using fear-based decisions, pathfinding, and combat behavior — while zombies relentlessly hunt them down.

---

## 🎮 Description

This is an **AI vs AI simulation** game built using **Python** and **Pygame**, where:

- Humans use **pathfinding**, **fear mechanics**, and **combat behavior** to survive.
- Zombies **chase and convert** humans using aggression-driven AI.
- The environment features **obstacles**, **safe zones**, **dynamic spawning**, and **time-based victory conditions**.

Humans must survive for **60 seconds**. If all are turned into zombies, the horde wins!

---

## ✨ Features

- 🤖 **Autonomous Agents**: Both humans and zombies make their own decisions based on the game state.
- 🚷 **Obstacle Avoidance**: Grid-based pathfinding for realistic movement.
- 🔫 **Combat System**: Humans shoot zombies with limited ammo and reloading time.
- 🧠 **Fear System**: Humans flee or seek safe zones when overwhelmed.
- 🩸 **Visual Effects**: Blood splatters, health bars, and directional sprites.
- 🧟‍♀️ **Zombie Conversion**: Caught humans are turned into zombies.
- ⏱️ **Time-Based Victory**: Humans win if at least one survives for 60 seconds.
- 🌱 **Dynamic Spawning**: New zombies spawn over time to increase difficulty.

---

## 📦 Requirements

- Python 3.x
- [Pygame](https://www.pygame.org/) library

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Maruthi5760/maruthi
cd ai-zombie-survival
```

Install dependencies:

```bash
pip install pygame
```

Run the game:

```bash
python zom_surv.py
```

---

## 🎮 Controls

| Key | Action                  |
|-----|-------------------------|
| `ESC` | Quit the game         |
| `R`   | Restart after Game Over |

---

## 🧠 Game Rules

- ✅ **Humans Win**: If at least one human survives for **60 seconds**
- ❌ **Zombies Win**: If **all humans** are converted

---

## 🧍‍♂️ Human Behavior

- 🧠 Uses A* pathfinding to move
- 🏃‍♂️ Flees when zombies are too close
- 🧍‍♂️ Seeks safe zones when scared
- 🔫 Shoots nearby zombies (limited ammo)
- ⏳ Reloads when out of bullets

---

## 🧟 Zombie Behavior

- 🧠 Pathfinds to the nearest human
- 😈 Becomes aggressive near prey
- 💀 Converts humans upon contact

---

## 🛠️ Customization

Modify constants in `zom_surv.py` to tweak game behavior:

| Constant        | Description                       |
|----------------|-----------------------------------|
| `WIDTH`, `HEIGHT` | Screen size                   |
| `FPS`             | Frame rate / game speed       |
| `HUMAN_SPEED`     | Human movement speed          |
| `ZOMBIE_SPEED`    | Zombie movement speed         |
| `BULLET_SPEED`    | Bullet travel speed           |
| `SPAWN_RATE`      | How often zombies appear      |
| `GAME_DURATION`   | Time humans must survive      |

---

## 🔮 Future Improvements

- Different human/zombie types with special abilities
- Weapons and collectible items
- Sound effects and background music
- More complex maps (e.g., choke points, barricades)
- Difficulty settings and dynamic scaling

---

## 📁 Assets

The game uses `.png` image files for humans, zombies, bullets, and background. If the images are not found, Pygame will automatically draw basic shapes for game elements.

Make sure the `assets/` folder is present and contains:

- `human.png`
- `zombie.png`
- `bullet.png`
- `background.png` (optional)

---

## 🧑‍💻 Credits

Created by **Maruthi** using **Python** and **Pygame**.

---

## 🧠 Enjoy watching the AI battle it out!
Humans panic, zombies attack, and only one species will survive. Can AI outsmart AI?

---
