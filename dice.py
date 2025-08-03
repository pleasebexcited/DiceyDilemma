import pygame
import math

class Dice:
    def __init__(self, index, value, is_wild=False):
        self.index = index
        self.value = value
        self.is_wild = is_wild
        self.size = 100  # Increased dice size from 80 to 100
        self.selected = False
        
        # Calculate position based on index (2 rows of 3 dice) - aligned with health bar edges
        row = index // 3
        col = index % 3
        
        # Center the dice horizontally on screen but align with health bar edges
        # Available width: 400px, health bars are 140px wide
        # Health bars start at x=50 and x=250, so dice should align with those edges
        start_x = 30  # Align with reroll counter and health bar edge
        gap = 25  # Increased gap to match power-ups
        row_gap = 15  # Reduced gap between rows (was 20)
        
        self.x = start_x + col * (self.size + gap)
        self.y = 250 + row * (self.size + row_gap)  # Moved down from 230 to 250
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        
        # Colors
        self.bg_color = (255, 255, 255)  # White
        self.border_color = (100, 100, 100)  # Gray
        self.selected_color = (255, 255, 0)  # Yellow
        self.dot_color = (0, 0, 0)  # Black
        self.star_color = (255, 215, 0)  # Gold
    
    def draw(self, screen, is_selected):
        """Draw the die"""
        # Draw background
        if is_selected:
            pygame.draw.rect(screen, self.selected_color, self.rect)
        else:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, 3)
        
        if self.is_wild:
            self.draw_star(screen)
        else:
            self.draw_dots(screen)
    
    def draw_dots(self, screen):
        """Draw dots on the die based on value"""
        dot_radius = 5  # Slightly larger dots for bigger dice
        margin = 12  # More margin for bigger dice
        
        # Define dot positions for each value
        dot_positions = {
            1: [(0.5, 0.5)],
            2: [(0.25, 0.25), (0.75, 0.75)],
            3: [(0.25, 0.25), (0.5, 0.5), (0.75, 0.75)],
            4: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.75), (0.75, 0.75)],
            5: [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)],
            6: [(0.25, 0.25), (0.75, 0.25), (0.25, 0.5), (0.75, 0.5), (0.25, 0.75), (0.75, 0.75)]
        }
        
        if self.value in dot_positions:
            for rel_x, rel_y in dot_positions[self.value]:
                x = self.x + margin + (self.size - 2 * margin) * rel_x
                y = self.y + margin + (self.size - 2 * margin) * rel_y
                pygame.draw.circle(screen, self.dot_color, (int(x), int(y)), dot_radius)
    
    def draw_star(self, screen):
        """Draw a star for wild card dice"""
        center_x = self.x + self.size // 2
        center_y = self.y + self.size // 2
        radius = 20  # Larger star for bigger dice
        
        # Draw a simple star (5-pointed)
        points = []
        for i in range(10):
            angle = i * math.pi / 5
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.4
            x = center_x + r * math.cos(angle)
            y = center_y + r * math.sin(angle)
            points.append((x, y))
        
        if len(points) >= 3:
            pygame.draw.polygon(screen, self.star_color, points) 