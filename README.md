<<<<<<< HEAD
# Dicey Dilemma

A roguelike dice game where you battle fantasy creatures using strategic dice combinations!

## Description

Dicey Dilemma is a turn-based combat game where you roll 6 dice and create the best possible combinations to deal damage to enemies. Progress through increasingly difficult levels, defeat various fantasy creatures, and try to achieve the highest level possible!

## Features

- **Strategic Dice Rolling**: Roll 6 dice and strategically reroll to create the best combinations
- **Reroll System**: 3 rerolls per hand that reset after each play
- **Gold Currency**: Earn gold by defeating enemies, with higher levels giving more rewards
- **Shield System**: Shield absorbs damage before health, refills after each level
- **Multiple Scoring Combinations**: Pairs, triples, straights, and more!
- **Wild Card Dice**: Special star dice that can be any number (15% chance per die)
- **Progressive Difficulty**: Enemies get stronger with each level
- **Health System**: Manage your health and heal after defeating enemies
- **High Score Tracking**: Save your best level reached
- **Mobile-Friendly Design**: Optimized for touch and mouse interaction

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. Run the game:
   ```bash
   python main.py
   ```

2. **Game Controls**:
   - **Mouse/Touch**: Click dice to select them for rerolling
   - **Roll Button**: Roll 6 new dice
   - **Discard Button**: Reroll selected dice (3 rerolls per hand)
   - **Play Button**: Use current dice hand to attack enemy

3. **Gameplay**:
   - Start by clicking "Roll" to get your initial 6 dice
   - Click on dice you want to reroll (they'll turn yellow)
   - Click "Discard" to reroll selected dice (uses 1 of 3 rerolls)
   - Click "Play" when you're happy with your hand
   - Your score becomes damage dealt to the enemy
   - After each play, your 3 rerolls are reset for the next hand
   - Enemy takes their turn and attacks you
   - Defeat enemies to progress to the next level
   - Heal 15% of max health, earn gold, and restore shield after each victory

## Scoring Rules

### Base Combinations:
- **Two Sequential Numbers** (e.g., 1,2): 200 points
- **Three Sequential Numbers** (e.g., 3,4,5): 300 points
- **Four Sequential Numbers** (e.g., 2,3,4,5): 400 points
- **Five Sequential Numbers** (e.g., 2,3,4,5,6): 500 points
- **Six Sequential Numbers** (e.g., 1,2,3,4,5,6): 1000 points

- **Pair** (e.g., 1,1): 100 points
- **Triple** (e.g., 1,1,1): 200 points
- **Four of a Kind** (e.g., 1,1,1,1): 400 points
- **Five of a Kind** (e.g., 1,1,1,1,1): 500 points
- **Six of a Kind** (e.g., 1,1,1,1,1,1): 600 points
- **Two Pair** (e.g., 1,1,2,2): 500 points
- **Full House** (three of a kind + pair): 600 points

### Bonus Points:
- **1's in scoring combination**: +100 points each
- **2's in scoring combination**: +200 points each
- **3's in scoring combination**: +300 points each
- **4's in scoring combination**: +400 points each
- **5's in scoring combination**: +500 points each
- **6's in scoring combination**: +600 points each

### Wild Card Dice:
- Star dice (⭐) can be any number 1-6
- Automatically chooses the best value for maximum score
- 15% chance to appear on each die roll

## Game Mechanics

- **Health**: Player starts with 25000 HP, enemies start with 15000 HP
- **Shield**: Both player and enemies start with 100/100 shield that absorbs damage first
- **Enemy Progression**: Enemy health increases by 15% each level
- **Enemy Types**: Dragon, Goblin, Orc, Troll, Demon, Giant (random selection)
- **Reroll System**: 3 rerolls per hand that reset after each play
- **Gold System**: Earn gold by defeating enemies (base 50 + level bonus + enemy health bonus)
- **Healing**: 15% of max health restored after defeating an enemy
- **Shield Restoration**: Shield refills to 100/100 after defeating an enemy
- **Game Over**: When player health reaches 0

## File Structure

- `main.py` - Main game entry point
- `game.py` - Core game logic and state management
- `dice.py` - Dice rendering and behavior
- `scoring.py` - Scoring system and combination detection
- `player.py` - Player health and damage management
- `enemy.py` - Enemy types and health management
- `ui.py` - User interface and rendering
- `requirements.txt` - Python dependencies

## Tips for Success

1. **Prioritize High Numbers**: Higher numbers give more bonus points
2. **Use Wild Cards Wisely**: Star dice can create powerful combinations
3. **Plan Your Rerolls**: Don't waste rerolls on mediocre hands
4. **Watch Enemy Health**: Sometimes it's better to play a safe hand than risk a big one
5. **Manage Your Health**: The 15% healing after victories is crucial for survival

## Future Enhancements

- Sound effects and background music
- More enemy types with special abilities
- Power-ups and special dice
- Achievement system
- Different game modes

Enjoy playing Dicey Dilemma! May the dice be ever in your favor! 🎲⚔️ 
=======
# DiceyDilemma
A dice-based combat game with power-ups and 16-bit sound effects
>>>>>>> 91d062db8be89582ef486a52a83dded9471bc51f
