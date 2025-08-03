import pygame
import math
import random # Added for glitch effect

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 48)
        self.large_font = pygame.font.Font(None, 36)
        self.medium_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Colors
        self.title_color = (255, 215, 0)  # Gold
        self.text_color = (255, 255, 255)  # White
        self.button_color = (100, 100, 200)  # Blue
        self.button_hover_color = (150, 150, 255)  # Light blue
        self.health_green = (0, 255, 0)  # Green
        self.health_yellow = (255, 255, 0)  # Yellow
        self.health_red = (255, 0, 0)  # Red
        self.background_color = (20, 20, 40)  # Dark blue
        
        # Load enemy image
        try:
            self.dragon_image = pygame.image.load("images/dragon.png")
            # Scale the image to fit nicely (180x180 pixels) - smaller to prevent cutoff
            self.dragon_image = pygame.transform.scale(self.dragon_image, (180, 180))
        except:
            self.dragon_image = None
            print("Warning: Could not load dragon.png image")
        
        # Load player image
        try:
            self.knight_image = pygame.image.load("images/knight.jpg")
            # Scale the image to match health bar width (140px) while maintaining aspect ratio
            # Get original dimensions
            original_width, original_height = self.knight_image.get_size()
            # Calculate scale factor to match health bar width (140px)
            scale_factor = 140 / original_width
            new_width = 140
            new_height = int(original_height * scale_factor)
            self.knight_image = pygame.transform.scale(self.knight_image, (new_width, new_height))
        except:
            self.knight_image = None
            print("Warning: Could not load knight.jpg image")
        
        # Button rectangles - aligned with dice margins
        self.start_button = pygame.Rect(width//2 - 100, height - 120, 200, 50)
        self.restart_button = pygame.Rect(width//2 - 100, height - 120, 200, 50)
        
        # Calculate button positioning to match the power-up box alignment
        button_width = 100  # Match power-up width
        button_height = 50  # Slightly shorter than power-ups
        gap = 25  # Match power-up gap
        
        # Use same alignment logic as power-up boxes
        start_x = 30  # Align with the power-up boxes
        
        # Position buttons below the power-up boxes
        # Power-up boxes end at y=490 + 60 + 15 = 565, so buttons start at y=565 + 25 = 590
        button_y = 650  # Moved down from 590 to 650
        
        self.roll_button = pygame.Rect(start_x, button_y, button_width, button_height)
        self.discard_button = pygame.Rect(start_x + button_width + gap, button_y, button_width, button_height)
        self.play_button = pygame.Rect(start_x + 2 * (button_width + gap), button_y, button_width, button_height)
        
        # Power-up boxes - 6 rectangles in 2 rows of 3, same width and spacing as dice
        self.power_up_boxes = []
        power_up_width = 100  # Increased width for better alignment
        power_up_height = 60  # Increased height for better proportions
        gap = 25  # Increased gap for better spacing
        
        # Calculate positioning to match the reroll/gold line alignment
        # Reroll counter starts at x=30, so align power-ups with that
        start_x = 30  # Align with the reroll counter
        
        # Create 6 power-up boxes in 2 rows of 3
        for row in range(2):
            for col in range(3):
                x = start_x + col * (power_up_width + gap)
                # Position below the dice (dice end around y=430) and above buttons
                # Start at 490 to give proper space after the second row of dice
                y = 490 + row * (power_up_height + 15)  # Adjusted for new dice position
                box = pygame.Rect(x, y, power_up_width, power_up_height)
                self.power_up_boxes.append(box)
    
    def draw_menu(self, screen, high_score):
        """Draw the main menu"""
        # Title
        title_text = self.title_font.render("Dicey Dilemma", True, self.title_color)
        title_rect = title_text.get_rect(center=(self.width//2, 120))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.medium_font.render("A Roguelike Dice Adventure", True, self.text_color)
        subtitle_rect = subtitle_text.get_rect(center=(self.width//2, 160))
        screen.blit(subtitle_text, subtitle_rect)
        
        # High score
        if high_score > 0:
            high_score_text = self.medium_font.render(f"High Score: Level {high_score}", True, self.text_color)
            high_score_rect = high_score_text.get_rect(center=(self.width//2, 200))
            screen.blit(high_score_text, high_score_rect)
        
        # Instructions - better spaced
        instructions = [
            "Roll 6 dice and create the best combination!",
            "Click dice to select them for rerolling",
            "Sequential numbers and pairs score points",
            "Higher numbers give bonus points",
            "Defeat enemies to progress through levels"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, self.text_color)
            text_rect = text.get_rect(center=(self.width//2, 280 + i * 25))
            screen.blit(text, text_rect)
        
        # Start button
        pygame.draw.rect(screen, self.button_color, self.start_button)
        start_text = self.large_font.render("START", True, self.text_color)
        start_text_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_text_rect)
    
    def draw_shield_bar(self, screen, x, y, current_shield, max_shield, name):
        """Draw a shield bar"""
        bar_width = 140
        bar_height = 20
        
        # Center the shield bar under the health bar
        character_center_x = x + 50  # Character circle center
        bar_x = character_center_x - bar_width//2  # Perfect center alignment
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, y, bar_width, bar_height))
        
        # Shield percentage
        shield_percent = current_shield / max_shield
        
        # Shield color (blue)
        shield_color = (100, 150, 255)  # Light blue
        
        # Shield bar
        shield_width = int(bar_width * shield_percent)
        pygame.draw.rect(screen, shield_color, (bar_x, y, shield_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, y, bar_width, bar_height), 2)
        
        # Shield text
        shield_text = f"{current_shield}/{max_shield}"
        text_surface = self.small_font.render(shield_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(character_center_x, y + bar_height//2))
        screen.blit(text_surface, text_rect)
    
    def draw_combatants(self, screen, player, enemy, enemy_glitch_timer=0, player_glitch_timer=0, glitch_intensity=0):
        """Draw player and enemy with health bars"""
        # Player (left side) - moved up and width adjusted
        self.draw_character(screen, 50, 10, "Player", (100, 150, 255), is_enemy=False, glitch_timer=player_glitch_timer, glitch_intensity=glitch_intensity)  # Moved from 20 to 10
        self.draw_health_bar(screen, 50, 160, player.health, player.max_health, "Player")  # Moved from 120 to 140
        self.draw_shield_bar(screen, 50, 190, player.shield, player.max_shield, "Player")  # Moved from 150 to 170
        
        # Enemy (right side) - moved up
        self.draw_character(screen, 250, 10, enemy.enemy_type, (255, 100, 100), is_enemy=True, glitch_timer=enemy_glitch_timer, glitch_intensity=glitch_intensity)  # Moved from 20 to 10
        self.draw_health_bar(screen, 250, 160, enemy.health, enemy.max_health, enemy.enemy_type)  # Moved from 120 to 140
        self.draw_shield_bar(screen, 250, 190, enemy.shield, enemy.max_shield, enemy.enemy_type)  # Moved from 150 to 170
    
    def draw_character(self, screen, x, y, name, color, is_enemy=False, glitch_timer=0, glitch_intensity=0):
        """Draw a simple character representation with optional glitch effect"""
        character_center_x = x + 50
        
        if is_enemy and self.dragon_image:
            # Draw enemy image (dragon) - moved down
            image_rect = self.dragon_image.get_rect(center=(character_center_x, y + 80))  # Moved from y+50 to y+80
            
            # Apply glitch effect if active
            if glitch_timer > 0:
                # Create glitch effect by offsetting the image slightly
                offset_x = random.randint(-glitch_intensity, glitch_intensity)
                offset_y = random.randint(-glitch_intensity, glitch_intensity)
                glitch_rect = image_rect.copy()
                glitch_rect.x += offset_x
                glitch_rect.y += offset_y
                screen.blit(self.dragon_image, glitch_rect)
            else:
                screen.blit(self.dragon_image, image_rect)
        elif not is_enemy and self.knight_image:
            # Draw player image (knight) - moved down
            image_rect = self.knight_image.get_rect(center=(character_center_x, y + 80))  # Moved from y+50 to y+80
            
            # Apply glitch effect if active
            if glitch_timer > 0:
                # Create glitch effect by offsetting the image slightly
                offset_x = random.randint(-glitch_intensity, glitch_intensity)
                offset_y = random.randint(-glitch_intensity, glitch_intensity)
                glitch_rect = image_rect.copy()
                glitch_rect.x += offset_x
                glitch_rect.y += offset_y
                screen.blit(self.knight_image, glitch_rect)
            else:
                screen.blit(self.knight_image, image_rect)
        else:
            # Fallback to circle if image not available
            pygame.draw.circle(screen, color, (character_center_x, y + 80), 30)  # Moved from y+50 to y+80
        
        # Removed character name text
    
    def draw_health_bar(self, screen, x, y, current_health, max_health, name):
        """Draw a health bar"""
        bar_width = 140
        bar_height = 20
        
        # Center the health bar under the character
        character_center_x = x + 50  # Character circle center
        bar_x = character_center_x - bar_width//2  # Perfect center alignment
        
        # Background
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, y, bar_width, bar_height))
        
        # Health percentage
        health_percent = current_health / max_health
        
        # Health color based on percentage
        if health_percent > 0.6:
            health_color = self.health_green
        elif health_percent > 0.3:
            health_color = self.health_yellow
        else:
            health_color = self.health_red
        
        # Health bar
        health_width = int(bar_width * health_percent)
        pygame.draw.rect(screen, health_color, (bar_x, y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (bar_x, y, bar_width, bar_height), 2)
        
        # Health text
        health_text = f"{current_health}/{max_health}"
        text_surface = self.small_font.render(health_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(character_center_x, y + bar_height//2))
        screen.blit(text_surface, text_rect)
    
    def draw_power_up_boxes(self, screen, player=None, active_power_up=None):
        """Draw the power-up boxes"""
        for i, box in enumerate(self.power_up_boxes):
            # Check if this slot has a power-up
            if player and i < len(player.power_ups) and player.power_ups[i] is not None:
                power_up = player.power_ups[i]
                
                # Highlight if this power-up is currently active
                if active_power_up and power_up["name"] == active_power_up:
                    pygame.draw.rect(screen, (255, 255, 0), box)  # Yellow highlight
                    pygame.draw.rect(screen, (255, 255, 255), box, 3)  # Thick white border
                else:
                    pygame.draw.rect(screen, (80, 80, 80), box)  # Gray background
                    pygame.draw.rect(screen, (255, 255, 255), box, 2)  # White border
                
                # Draw power-up name (shortened if needed)
                name = power_up["name"]
                if len(name) > 8:  # Truncate long names
                    name = name[:8] + "..."
                
                # Draw dominos icon for "Line 'em up"
                if power_up["name"] == "Line 'em up":
                    # Draw 6 small rectangles to represent dominos
                    domino_width = 8
                    domino_height = 12
                    start_x = box.centerx - (domino_width * 3) // 2
                    start_y = box.centery - 15
                    
                    for j in range(6):
                        domino_x = start_x + (j % 3) * (domino_width + 2)
                        domino_y = start_y + (j // 3) * (domino_height + 2)
                        pygame.draw.rect(screen, (255, 255, 255), (domino_x, domino_y, domino_width, domino_height))
                        pygame.draw.rect(screen, (0, 0, 0), (domino_x, domino_y, domino_width, domino_height), 1)
                
                # Draw power-up name
                text = self.small_font.render(name, True, self.text_color)
                text_rect = text.get_rect(center=(box.centerx, box.bottom - 15))
                screen.blit(text, text_rect)
            else:
                # Power Up text for empty slots
                pygame.draw.rect(screen, (80, 80, 80), box)  # Gray background
                pygame.draw.rect(screen, (255, 255, 255), box, 2)  # White border
                text = self.small_font.render("Power Up", True, self.text_color)
                text_rect = text.get_rect(center=box.center)
                screen.blit(text, text_rect)
    
    def draw_game_ui(self, screen, rerolls_left, dice_rolled, selected_dice, player):
        """Draw the game UI elements"""
        # Draw rerolls and gold
        rerolls_text = self.medium_font.render(f"Rerolls: {rerolls_left}", True, self.text_color)
        gold_text = self.medium_font.render(f"Gold: {player.get_gold()}", True, self.text_color)
        
        # Position them side by side
        rerolls_rect = rerolls_text.get_rect()
        gold_rect = gold_text.get_rect()
        
        rerolls_rect.topleft = (30, 230)  # Fixed position
        gold_rect.topleft = (230, 230)  # Aligned with enemy shield bar left edge
        
        screen.blit(rerolls_text, rerolls_rect)
        screen.blit(gold_text, gold_rect)
        
        # Buttons
        self.draw_button(screen, self.roll_button, "Roll", not dice_rolled)
        self.draw_button(screen, self.discard_button, "Discard", dice_rolled and rerolls_left > 0 and selected_dice)
        self.draw_button(screen, self.play_button, "Play", dice_rolled)
    
    def draw_button(self, screen, rect, text, enabled):
        """Draw a button"""
        if enabled:
            pygame.draw.rect(screen, self.button_color, rect)
        else:
            pygame.draw.rect(screen, (80, 80, 80), rect)  # Gray when disabled
        
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)  # White border
        
        button_text = self.medium_font.render(text, True, self.text_color)
        text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, text_rect)
    
    def draw_message(self, screen, message):
        """Draw a message in the center of the screen"""
        if message:
            # Create a semi-transparent background
            overlay = pygame.Surface((self.width, 80))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, self.height//2 - 40))
            
            # Split long messages into multiple lines
            words = message.split()
            lines = []
            current_line = ""
            
            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_surface = self.small_font.render(test_line, True, self.text_color)
                if test_surface.get_width() <= self.width - 20:  # 10px margin on each side
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word
            
            if current_line:
                lines.append(current_line)
            
            # If no lines were created, use the original message
            if not lines:
                lines = [message]
            
            # Draw each line
            line_height = self.small_font.get_height()
            total_height = len(lines) * line_height
            start_y = self.height//2 - total_height//2
            
            for i, line in enumerate(lines):
                text_surface = self.small_font.render(line, True, self.text_color)
                text_rect = text_surface.get_rect(center=(self.width//2, start_y + i * line_height))
                screen.blit(text_surface, text_rect)
    
    def draw_game_over(self, screen, level_reached, high_score):
        """Draw the game over screen"""
        # Game over text
        game_over_text = self.title_font.render("Game Over!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.width//2, 150))
        screen.blit(game_over_text, game_over_rect)
        
        # Level reached
        level_text = self.large_font.render(f"Level Reached: {level_reached}", True, self.text_color)
        level_rect = level_text.get_rect(center=(self.width//2, 200))
        screen.blit(level_text, level_rect)
        
        # High score
        if level_reached >= high_score:
            new_record_text = self.medium_font.render("New High Score!", True, self.title_color)
            new_record_rect = new_record_text.get_rect(center=(self.width//2, 250))
            screen.blit(new_record_text, new_record_rect)
        else:
            high_score_text = self.medium_font.render(f"High Score: Level {high_score}", True, self.text_color)
            high_score_rect = high_score_text.get_rect(center=(self.width//2, 250))
            screen.blit(high_score_text, high_score_rect)
        
        # Restart button - positioned at bottom
        pygame.draw.rect(screen, self.button_color, self.restart_button)
        restart_text = self.large_font.render("Play Again", True, self.text_color)
        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        screen.blit(restart_text, restart_text_rect) 

    def draw_shop_ui(self, screen, player, shop_state):
        """Draw the shop interface overlay"""
        # Semi-transparent background overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Shop background
        shop_rect = pygame.Rect(20, 50, self.width - 40, self.height - 100)
        pygame.draw.rect(screen, (40, 40, 40), shop_rect)
        pygame.draw.rect(screen, (255, 255, 255), shop_rect, 3)
        
        # Shop title
        title_text = self.large_font.render("SHOP", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.width//2, 80))
        screen.blit(title_text, title_rect)
        
        # Gold display
        gold_text = self.medium_font.render(f"Gold: {player.get_gold()}", True, (255, 215, 0))
        gold_rect = gold_text.get_rect(center=(self.width//2, 120))
        screen.blit(gold_text, gold_rect)
        
        # Draw tabs
        self.draw_shop_tabs(screen, shop_state)
        
        # Draw shop content based on current tab
        if shop_state["current_tab"] == "buy":
            self.draw_buy_tab(screen, player, shop_state)
        elif shop_state["current_tab"] == "sell":
            self.draw_sell_tab(screen, player, shop_state)
        elif shop_state["current_tab"] == "upgrade":
            self.draw_upgrade_tab(screen, player, shop_state)
        elif shop_state["current_tab"] == "restore":
            self.draw_restore_tab(screen, player, shop_state)
        
        # Navigation buttons
        self.draw_shop_navigation(screen, shop_state)
    
    def draw_shop_tabs(self, screen, shop_state):
        """Draw the shop tabs"""
        tabs = ["buy", "sell", "upgrade", "restore"]
        tab_width = 80
        tab_height = 30
        start_x = 40
        
        for i, tab in enumerate(tabs):
            x = start_x + i * (tab_width + 5)
            y = 150
            
            # Tab background
            if shop_state["current_tab"] == tab:
                color = (100, 100, 100)  # Selected tab
            else:
                color = (60, 60, 60)  # Unselected tab
            
            tab_rect = pygame.Rect(x, y, tab_width, tab_height)
            pygame.draw.rect(screen, color, tab_rect)
            pygame.draw.rect(screen, (255, 255, 255), tab_rect, 2)
            
            # Tab text
            tab_text = self.small_font.render(tab.upper(), True, (255, 255, 255))
            text_rect = tab_text.get_rect(center=(x + tab_width//2, y + tab_height//2))
            screen.blit(tab_text, text_rect)
            
            # Store tab rect for click detection
            shop_state[f"{tab}_tab_rect"] = tab_rect
    
    def draw_buy_tab(self, screen, player, shop_state):
        """Draw the buy tab content"""
        y_start = 200
        
        # Line 'em up power-up
        power_up_cost = 50
        can_afford_power_up = player.get_gold() >= power_up_cost
        has_empty_slot = any(p is None for p in player.power_ups)
        
        # Item background
        item_rect = pygame.Rect(50, y_start, self.width - 100, 50)
        if can_afford_power_up and has_empty_slot:
            color = (80, 80, 80)
        else:
            color = (50, 50, 50)  # Greyed out
        pygame.draw.rect(screen, color, item_rect)
        pygame.draw.rect(screen, (255, 255, 255), item_rect, 2)
        
        # Item text
        text_color = (255, 255, 255) if can_afford_power_up and has_empty_slot else (150, 150, 150)
        item_text = self.medium_font.render("Line 'em up", True, text_color)
        cost_text = self.small_font.render(f"Cost: {power_up_cost} gold", True, text_color)
        desc_text = self.small_font.render("Six in a row = Double damage!", True, text_color)
        
        screen.blit(item_text, (70, y_start + 5))
        screen.blit(cost_text, (70, y_start + 25))
        screen.blit(desc_text, (70, y_start + 40))
        
        # Store rect for click detection
        shop_state["line_em_up_rect"] = item_rect
        shop_state["can_afford_line_em_up"] = can_afford_power_up and has_empty_slot
    
    def draw_sell_tab(self, screen, player, shop_state):
        """Draw the sell tab content"""
        # Placeholder for sell items
        y_start = 200
        item_text = self.medium_font.render("Sell items will be implemented here", True, (255, 255, 255))
        screen.blit(item_text, (50, y_start))
    
    def draw_upgrade_tab(self, screen, player, shop_state):
        """Draw the upgrade tab content"""
        # Placeholder for upgrade items
        y_start = 200
        item_text = self.medium_font.render("Upgrade items will be implemented here", True, (255, 255, 255))
        screen.blit(item_text, (50, y_start))
    
    def draw_restore_tab(self, screen, player, shop_state):
        """Draw the restore tab content"""
        y_start = 200
        
        # Health restoration item
        health_cost = 150
        can_afford_health = player.get_gold() >= health_cost
        
        # Item background
        item_rect = pygame.Rect(50, y_start, self.width - 100, 50)
        if can_afford_health:
            color = (80, 80, 80)
        else:
            color = (50, 50, 50)  # Greyed out
        pygame.draw.rect(screen, color, item_rect)
        pygame.draw.rect(screen, (255, 255, 255), item_rect, 2)
        
        # Item text
        text_color = (255, 255, 255) if can_afford_health else (150, 150, 150)
        item_text = self.medium_font.render("Restore 30% Health", True, text_color)
        cost_text = self.small_font.render(f"Cost: {health_cost} gold", True, text_color)
        
        screen.blit(item_text, (70, y_start + 10))
        screen.blit(cost_text, (70, y_start + 30))
        
        # Store rect for click detection
        shop_state["health_restore_rect"] = item_rect
        shop_state["can_afford_health"] = can_afford_health
    
    def draw_shop_navigation(self, screen, shop_state):
        """Draw shop navigation buttons"""
        # Back button
        back_rect = pygame.Rect(50, self.height - 80, 80, 30)
        pygame.draw.rect(screen, (100, 100, 100), back_rect)
        pygame.draw.rect(screen, (255, 255, 255), back_rect, 2)
        
        back_text = self.small_font.render("BACK", True, (255, 255, 255))
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)
        
        # Continue button
        continue_rect = pygame.Rect(self.width - 130, self.height - 80, 80, 30)
        pygame.draw.rect(screen, (100, 150, 255), continue_rect)
        pygame.draw.rect(screen, (255, 255, 255), continue_rect, 2)
        
        continue_text = self.small_font.render("CONTINUE", True, (255, 255, 255))
        continue_text_rect = continue_text.get_rect(center=continue_rect.center)
        screen.blit(continue_text, continue_text_rect)
        
        # Store rects for click detection
        shop_state["back_button_rect"] = back_rect
        shop_state["continue_button_rect"] = continue_rect 