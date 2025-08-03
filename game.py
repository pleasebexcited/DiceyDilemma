import pygame
import random
import json
import os
from dice import Dice
from enemy import Enemy
from player import Player
from ui import UI
from scoring import ScoringSystem

class DiceyDilemma:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Initialize pygame mixer for sound
        try:
            pygame.mixer.init()
            self.audio_available = True
        except:
            # If audio initialization fails, continue without sound
            self.audio_available = False
        
        # Load sound effects
        self.attack_sound = None
        self.power_up_sound = None
        self.death_sound = None
        try:
            # Try to load sound files if they exist and audio is available
            if hasattr(self, 'audio_available') and self.audio_available:
                if os.path.exists("sounds/attack.wav"):
                    self.attack_sound = pygame.mixer.Sound("sounds/attack.wav")
                if os.path.exists("sounds/power_up.wav"):
                    self.power_up_sound = pygame.mixer.Sound("sounds/power_up.wav")
                if os.path.exists("sounds/death.wav"):
                    self.death_sound = pygame.mixer.Sound("sounds/death.wav")
        except:
            # If sound loading fails, continue without sound
            pass
        
        # Initialize game components
        self.player = Player(25000)  # Increased from 5000 to accommodate new enemy damage
        self.enemy = None
        self.dice = []
        self.ui = UI(self.width, self.height)
        self.scoring_system = ScoringSystem()
        
        # Game state
        self.game_state = "menu"  # menu, playing, enemy_turn, game_over, victory, shop
        self.current_level = 1
        self.rerolls_left = 3
        self.selected_dice = []
        self.dice_rolled = False
        self.enemy_turn_timer = 0
        self.display_message = ""
        self.message_timer = 0
        
        # Shop state (new)
        self.shop_state = {
            "current_tab": "restore",
            "active": False
        }
        
        # Animation timers
        self.enemy_glitch_timer = 0
        self.player_glitch_timer = 0
        self.glitch_intensity = 0
        self.double_damage_timer = 0
        self.second_attack_timer = 0
        self.second_attack_score = 0
        self.second_attack_message = ""
        self.attack_count = 0
        
        # Load high score
        self.high_score = self.load_high_score()
        
        # Initialize first enemy
        self.spawn_new_enemy()
        
        # Initialize dice
        self.roll_dice()
    
    def spawn_new_enemy(self):
        """Spawn a new enemy with increasing health"""
        base_health = 15000  # Increased from 3000 to accommodate new scoring
        health_increase = 1.15 ** (self.current_level - 1)  # Increased from 1.1 to 1.15 for steeper scaling
        enemy_health = int(base_health * health_increase)
        
        enemy_types = ["Dragon", "Goblin", "Orc", "Troll", "Demon", "Giant"]
        enemy_type = random.choice(enemy_types)
        
        self.enemy = Enemy(enemy_type, enemy_health)
        self.rerolls_left = 3
        self.dice_rolled = False
    
    def roll_dice(self):
        """Roll 6 dice with 15% chance for wild card"""
        self.dice = []
        for i in range(6):
            if random.random() < 0.15:  # 15% chance for wild card
                die = Dice(i, 0, is_wild=True)
            else:
                value = random.randint(1, 6)
                die = Dice(i, value, is_wild=False)
            self.dice.append(die)
        self.dice_rolled = True
        self.selected_dice = []
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self.handle_click(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.game_state == "playing":
                self.roll_dice()
            elif event.key == pygame.K_RETURN and self.game_state == "menu":
                self.game_state = "playing"
    
    def handle_shop_click(self, pos):
        """Handle clicks in the shop interface"""
        x, y = pos
        
        # Check tab clicks
        for tab in ["buy", "sell", "upgrade", "restore"]:
            if f"{tab}_tab_rect" in self.shop_state:
                if self.shop_state[f"{tab}_tab_rect"].collidepoint(x, y):
                    self.shop_state["current_tab"] = tab
                    return
        
        # Check navigation buttons
        if "back_button_rect" in self.shop_state and self.shop_state["back_button_rect"].collidepoint(x, y):
            # Go back to game (could be used for other functionality later)
            return
        
        if "continue_button_rect" in self.shop_state and self.shop_state["continue_button_rect"].collidepoint(x, y):
            # Continue to next level
            self.shop_state["active"] = False
            self.game_state = "playing"
            self.current_level += 1  # Increment level
            self.spawn_new_enemy()
            self.roll_dice()
            return
        
        # Check restore tab items
        if self.shop_state["current_tab"] == "restore":
            if "health_restore_rect" in self.shop_state and self.shop_state["health_restore_rect"].collidepoint(x, y):
                if self.shop_state.get("can_afford_health", False):
                    # Purchase health restoration
                    self.player.spend_gold(150)
                    heal_amount = int(self.player.max_health * 0.3)
                    self.player.heal(heal_amount)
                    self.display_message = f"Health restored! +{heal_amount} HP"
                    self.message_timer = 120  # 2 seconds
                    return
        
        # Check buy tab items
        if self.shop_state["current_tab"] == "buy":
            if "line_em_up_rect" in self.shop_state and self.shop_state["line_em_up_rect"].collidepoint(x, y):
                if self.shop_state.get("can_afford_line_em_up", False):
                    # Purchase Line 'em up power-up
                    self.player.spend_gold(50)
                    power_up = {
                        "name": "Line 'em up",
                        "description": "Six in a row = Double damage!",
                        "cost": 50
                    }
                    if self.player.add_power_up(power_up):
                        self.display_message = "Line 'em up power-up purchased!"
                        self.message_timer = 120  # 2 seconds
                    else:
                        self.display_message = "No empty power-up slots!"
                        self.message_timer = 120  # 2 seconds
                    return
    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Handle shop clicks first
        if self.game_state == "shop":
            self.handle_shop_click(pos)
            return
        
        if self.game_state == "playing":
            # Check if dice were clicked
            for i, die in enumerate(self.dice):
                if die.rect.collidepoint(pos):
                    if i in self.selected_dice:
                        self.selected_dice.remove(i)
                    else:
                        self.selected_dice.append(i)
                    break
            
            # Check if buttons were clicked
            if self.ui.roll_button.collidepoint(pos) and not self.dice_rolled:
                self.roll_dice()
            elif self.ui.discard_button.collidepoint(pos) and self.dice_rolled and self.rerolls_left > 0:
                self.discard_selected_dice()
            elif self.ui.play_button.collidepoint(pos) and self.dice_rolled:
                self.play_hand()
        
        elif self.game_state == "menu":
            if self.ui.start_button.collidepoint(pos):
                self.game_state = "playing"
        
        elif self.game_state == "game_over":
            if self.ui.restart_button.collidepoint(pos):
                self.restart_game()
    
    def discard_selected_dice(self):
        """Discard selected dice and reroll them"""
        if self.rerolls_left > 0 and self.selected_dice:
            for i in self.selected_dice:
                if random.random() < 0.15:  # 15% chance for wild card
                    self.dice[i] = Dice(i, 0, is_wild=True)
                else:
                    value = random.randint(1, 6)
                    self.dice[i] = Dice(i, value, is_wild=False)
            
            self.rerolls_left -= 1
            self.selected_dice = []
    
    def play_attack_sound(self, is_power_up=False, is_death=False):
        """Play attack sound effect"""
        if not hasattr(self, 'audio_available') or not self.audio_available:
            return  # Skip sound if audio is not available
        
        try:
            if is_death and self.death_sound:
                self.death_sound.play()
            elif is_power_up and self.power_up_sound:
                self.power_up_sound.play()
            elif self.attack_sound:
                self.attack_sound.play()
        except:
            # If sound playing fails, continue silently
            pass
    
    def check_sequential_six(self, dice_values):
        """Check if dice show 1,2,3,4,5,6 in any order"""
        # Filter out wild dice (value 0) and get non-wild values
        non_wild_values = [v for v in dice_values if v != 0]
        wild_count = dice_values.count(0)
        
        # If we have wild dice, we need to check if the non-wild values can form a sequence
        # and the wild dice can fill in the missing numbers
        if wild_count > 0:
            # Sort the non-wild values
            sorted_non_wild = sorted(non_wild_values)
            
            # Check if we can form 1,2,3,4,5,6 with the available numbers and wild dice
            required_numbers = [1, 2, 3, 4, 5, 6]
            missing_numbers = []
            
            for num in required_numbers:
                if num not in sorted_non_wild:
                    missing_numbers.append(num)
            
            # If wild dice can fill all missing numbers, it's a sequential six
            return len(missing_numbers) <= wild_count
        else:
            # No wild dice, just check if we have 1,2,3,4,5,6
            sorted_values = sorted(dice_values)
            result = sorted_values == [1, 2, 3, 4, 5, 6]
            return result
    
    def play_hand(self):
        """Play the current dice hand"""
        # Calculate score
        dice_values = [die.value for die in self.dice]
        wild_dice = [i for i, die in enumerate(self.dice) if die.is_wild]
        
        score, scoring_hand, calculation = self.scoring_system.calculate_score(dice_values, wild_dice)
        
        # Deal damage to enemy
        self.enemy.take_damage(score)
        
        # Play attack sound
        self.play_attack_sound()
        
        # Trigger enemy glitch animation
        self.enemy_glitch_timer = 30  # 0.5 seconds at 60 FPS
        self.glitch_intensity = 15
        
        # Reset rerolls for next turn
        self.rerolls_left = 3
        
        # Display result
        self.display_message = f"{scoring_hand}: {calculation} = {score} damage!"
        self.message_timer = 180  # 3 seconds at 60 FPS
        
        # Check for "Line 'em up" power-up activation
        has_power_up = self.player.has_power_up("Line 'em up")
        is_sequential = self.check_sequential_six(dice_values)
        
        # Check if enemy is defeated
        if self.enemy.health <= 0:
            self.enemy_defeated()
        else:
            # Only start power-up attacks if enemy is still alive
            if has_power_up and is_sequential:
                # Count how many "Line 'em up" power-ups the player has
                power_up_count = self.player.get_power_up_count("Line 'em up")
                
                # Trigger first attack
                self.display_message = f"{scoring_hand}: {calculation} = {score} damage!"
                self.message_timer = 90  # 1.5 seconds for first attack
                
                # Set up multiple attacks based on power-up count
                self.second_attack_timer = 90  # 1.5 second delay before second attack
                self.second_attack_score = score
                self.second_attack_message = f"{scoring_hand}: {calculation} = {score} damage! + Line 'em up: Double damage!"
                self.attack_count = power_up_count  # Track how many attacks to perform
                
                # Keep power-up active during all attacks
                self.double_damage_timer = 90 + (power_up_count * 90)  # 1.5s per attack
            elif is_sequential:
                # Check if it was a sequential six but no power-up
                self.display_message = f"{scoring_hand}: {calculation} = {score} damage! (Sequential six - buy Line 'em up for double damage!)"
                self.message_timer = 180  # 3 seconds at 60 FPS
            else:
                # Only start enemy turn if no power-up attacks are pending
                if self.second_attack_timer == 0 and self.attack_count == 0:
                    self.game_state = "enemy_turn"
                    self.enemy_turn_timer = 60  # 1 second delay
                else:
                    # Keep in playing state until all attacks are complete
                    self.game_state = "playing"
    
    def enemy_turn(self):
        """Enemy's turn to roll and attack"""
        # Check if enemy is already defeated
        if self.enemy.health <= 0:
            self.enemy_defeated()
            return
        
        # Enemy rolls dice
        enemy_dice = []
        for i in range(6):
            if random.random() < 0.15:
                enemy_dice.append(0)  # Wild card
            else:
                enemy_dice.append(random.randint(1, 6))
        
        # Calculate enemy score
        score, scoring_hand, calculation = self.scoring_system.calculate_score(enemy_dice, [])
        
        # Deal damage to player
        self.player.take_damage(score)
        
        # Play enemy attack sound
        self.play_attack_sound()
        
        # Trigger player glitch animation
        self.player_glitch_timer = 30  # 0.5 seconds at 60 FPS
        self.glitch_intensity = 15
        
        # Display result
        self.display_message = f"Enemy {scoring_hand}: {calculation} = {score} damage!"
        self.message_timer = 180
        
        # Check if player is defeated
        if self.player.health <= 0:
            self.game_over()
        else:
            self.game_state = "playing"
            self.roll_dice()
    
    def enemy_defeated(self):
        """Handle enemy defeat"""
        # Play death sound
        self.play_attack_sound(is_death=True)
        
        # Calculate gold reward based on current level and enemy health
        # Higher levels and tougher enemies give more gold
        base_gold = 50  # Base gold per level
        level_bonus = self.current_level * 10  # More gold for higher levels
        enemy_health_bonus = self.enemy.max_health // 100  # Bonus based on enemy toughness
        
        gold_earned = base_gold + level_bonus + enemy_health_bonus
        self.player.earn_gold(gold_earned)
        
        # Heal player by 15%
        heal_amount = int(self.player.max_health * 0.15)
        self.player.heal(heal_amount)
        
        # Refill shield
        self.player.refill_shield()
        
        # Display victory message
        self.display_message = f"Enemy defeated! +{heal_amount} HP, +{gold_earned} Gold. Shield restored!"
        self.message_timer = 180  # 3 seconds
        
        # Open shop instead of immediately spawning new enemy
        self.game_state = "shop"
        self.shop_state["active"] = True
    
    def game_over(self):
        """Handle game over"""
        self.game_state = "game_over"
        self.display_message = f"Game Over! Level reached: {self.current_level}"
        self.message_timer = 300  # 5 seconds
    
    def restart_game(self):
        """Restart the game"""
        self.player = Player(25000)  # Increased from 5000 to accommodate new enemy damage
        self.current_level = 1
        self.spawn_new_enemy()
        self.roll_dice()
        self.game_state = "playing"
        self.display_message = ""
        self.message_timer = 0
    
    def update(self):
        """Update game state"""
        if self.game_state == "enemy_turn":
            self.enemy_turn_timer -= 1
            if self.enemy_turn_timer <= 0:
                self.enemy_turn()
        
        if self.message_timer > 0:
            self.message_timer -= 1
        
        # Update animation timers
        if self.enemy_glitch_timer > 0:
            self.enemy_glitch_timer -= 1
        if self.player_glitch_timer > 0:
            self.player_glitch_timer -= 1
        if self.glitch_intensity > 0:
            self.glitch_intensity -= 1
        if self.double_damage_timer > 0:
            self.double_damage_timer -= 1
        if self.second_attack_timer > 0:
            self.second_attack_timer -= 1
            # Trigger second attack when timer reaches 0
            if self.second_attack_timer == 0:
                # Check if enemy is still alive before attacking
                if self.enemy.health > 0:
                    # Deal additional damage
                    self.enemy.take_damage(self.second_attack_score)
                    
                    # Play power-up attack sound
                    self.play_attack_sound(is_power_up=True)
                    
                    # Trigger enemy glitch animation again
                    self.enemy_glitch_timer = 30  # 0.5 seconds at 60 FPS
                    self.glitch_intensity = 15
                    
                    # Show attack message
                    self.display_message = self.second_attack_message
                    self.message_timer = 90  # 1.5 seconds
                    
                    # If we have more attacks to perform, set up the next one
                    self.attack_count -= 1
                    if self.attack_count > 0:
                        self.second_attack_timer = 90  # 1.5 second delay before next attack
                    else:
                        # All attacks complete, start enemy turn
                        self.game_state = "enemy_turn"
                        self.enemy_turn_timer = 60  # 1 second delay
                else:
                    # Enemy is dead, stop power-up attacks and go to victory
                    self.enemy_defeated()
    
    def draw(self):
        """Draw the game"""
        self.screen.fill((0, 0, 0))  # Black background
        
        if self.game_state == "shop":
            # Draw game state behind shop
            self.draw_game()
            # Draw shop overlay
            self.ui.draw_shop_ui(self.screen, self.player, self.shop_state)
        elif self.game_state == "menu":
            self.ui.draw_menu(self.screen, self.high_score)
        elif self.game_state == "playing":
            self.draw_game()
        elif self.game_state == "enemy_turn":
            self.draw_game()
        elif self.game_state == "game_over":
            self.ui.draw_game_over(self.screen, self.current_level, self.high_score)
    
    def draw_game(self):
        """Draw the main game screen"""
        # Draw player and enemy
        self.ui.draw_combatants(self.screen, self.player, self.enemy, self.enemy_glitch_timer, self.player_glitch_timer, self.glitch_intensity)
        
        # Draw dice
        for die in self.dice:
            die.draw(self.screen, die.index in self.selected_dice)
        
        # Draw UI
        self.ui.draw_game_ui(self.screen, self.rerolls_left, self.dice_rolled, self.selected_dice, self.player)
        
        # Draw power-up boxes with active power-up highlighting
        active_power_up = None
        if self.double_damage_timer > 0 or self.second_attack_timer > 0:
            active_power_up = "Line 'em up"
        self.ui.draw_power_up_boxes(self.screen, self.player, active_power_up)
        
        # Draw message
        if self.message_timer > 0:
            self.ui.draw_message(self.screen, self.display_message)
    
    def load_high_score(self):
        """Load high score from file"""
        try:
            if os.path.exists("high_score.json"):
                with open("high_score.json", "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
        except:
            pass
        return 0
    
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open("high_score.json", "w") as f:
                json.dump({"high_score": self.high_score}, f)
        except:
            pass 