# Zombie Attack

2D survival shooter built in Python with Pygame.

**Winner of two Featured Project awards (Projeto Destaque) at Insper ExpoTech 2025: public vote and judging committee.**

[Gameplay video](https://youtu.be/nURn7oZUbBs) · [Project website](https://insper-classroom.github.io/projeto-pygame-site-time-preto-nader-e-murilo/)

## The game

A lone soldier must survive two minutes of a zombie wave while defending his military base. Two enemy types (slow brawlers that attack the player, fast runners that rush the base), aerial bombs falling at random, and a survivor ranking at the end.

Score = health + (shot accuracy % × 200) + (zombies killed × 2)

## How it's built

- Object-oriented structure: characters, enemies, bombs and each screen (start, name, instructions, game, victory, game over) in their own modules
- Sprite animations for movement, shooting, damage and death
- Mouse-aimed shooting: bullet angle follows the cursor, with fire cooldown and reload
- Collision detection between bullets, zombies, bombs and the player
- Timed enemy spawning at random positions, plus a countdown timer
- Persistent ranking stored in JSON
- Sound effects and HUD with health and ammo

## How to run

Requires Python 3.10+.

```bash
pip install pygame
python main.py
```

On Windows, set display scaling to 100%.

## Authors

Built by [Murilo Godoy](https://github.com/murilozgodoy) and [Nader Taha](https://github.com/nadertaha06) for the Developer Life course at Insper (2025).
