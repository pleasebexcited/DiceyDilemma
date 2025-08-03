import pygame
import sys
from game import DiceyDilemma

def main():
    """Main function to run the Dicey Dilemma game"""
    pygame.init()
    
    # Set up display for mobile aspect ratio (9:16)
    screen_width = 400
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Dicey Dilemma")
    
    # Initialize the game
    game = DiceyDilemma(screen)
    
    # Game loop
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 