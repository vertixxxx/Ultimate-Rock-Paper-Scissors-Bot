import pygame
import random
import sys
import model

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")
clock = pygame.time.Clock()

# Fonts
title_font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

class ChoiceSprite(pygame.sprite.Sprite):
    """A Pygame Sprite representing a playable choice (Rock, Paper, or Scissors)."""
    def __init__(self, name, x, y, color, font, text_color):
        super().__init__()
        self.name = name
        
        # Create a colored square surface for the sprite instead of loading an image
        self.image = pygame.Surface((150, 150))
        self.image.fill(color)
        
        # Render the name onto the center of the sprite
        text = font.render(name, True, text_color)
        text_rect = text.get_rect(center=(75, 75))
        self.image.blit(text, text_rect)
        
        # Set the rectangle for positioning and collision detection
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

def get_result(player, computer, p_score, c_score):
    """Determines the winner of the game and updates scores."""
    if player == computer:
        return "It's a Tie!", p_score, c_score
    
    if (player == "Rock" and computer == "Scissors") or \
       (player == "Paper" and computer == "Rock") or \
       (player == "Scissors" and computer == "Paper"):
            p_score += 1
            return "You Win!", p_score, c_score
    else: # Computer wins
        c_score += 1
        return "Computer Wins!", p_score, c_score

def main():
    # Create a Sprite Group to hold our clickable options
    choices = pygame.sprite.Group()

    # Instantiate the three sprites with different colors
    rock = ChoiceSprite("Rock", 100, 400, (255, 100, 100), small_font, BLACK)      # Reddish
    paper = ChoiceSprite("Paper", 325, 400, (100, 255, 100), small_font, BLACK)    # Greenish
    scissors = ChoiceSprite("Scissors", 550, 400, (100, 100, 255), small_font, BLACK) # Blueish

    choices.add(rock, paper, scissors)

    # Game variables
    options = ["Rock", "Paper", "Scissors"]
    player_choice = None
    computer_choice = None
    result_text = "Click a shape below to play!"
    p_score = 0
    c_score = 0
    
    running = True
    Markov1_bot = model.Markov1()
    Markov2_bot = model.Markov2()
    BayesianMarkov_bot = model.BayesianMarkov()
    #Strategy Pattern to choose bot
    bots = {
        "random": None,  # Special case or wrap in a simple class
        "markov1": Markov1_bot,
        "markov2": Markov2_bot,
        "bayesian": BayesianMarkov_bot
    }
    active_bot_key = "bayesian"


    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the user clicked on any of the sprites
                mouse_pos = pygame.mouse.get_pos()
                #print(Markov2_bot.transition_matrix)

                for sprite in choices:
                    if sprite.rect.collidepoint(mouse_pos):
                        player_choice = sprite.name
                        bot = bots[active_bot_key]
                        if bot is None:
                            computer_choice = random.choice(options)
                        else:
                            computer_choice = bot.predict_and_play()
                            bot.update(player_choice)

                        result_text, p_score, c_score = get_result(player_choice, computer_choice, p_score, c_score)

        # 2. Draw Background
        screen.fill(WHITE)

        # 3. Draw Sprites
        choices.draw(screen)

        # 4. Draw UI Text
        if player_choice and computer_choice:
            p_text = title_font.render(f"You: {player_choice}", True, BLACK)
            c_text = title_font.render(f"Computer: {computer_choice}", True, BLACK)
            r_text = title_font.render(result_text, True, (200, 0, 0)) # Red text for the result
            score_text = title_font.render(f"{p_score}-{c_score}", True, (0, 0, 0)) 
            
            screen.blit(p_text, (50, 100))
            screen.blit(c_text, (450, 100))
            screen.blit(r_text, (WIDTH // 2 - r_text.get_width() // 2, 250))
            screen.blit(score_text, (WIDTH // 2 - score_text.get_width()//2, 200))

        else:
            intro_text = title_font.render(result_text, True, BLACK)
            screen.blit(intro_text, (WIDTH // 2 - intro_text.get_width() // 2, 200))

        # 5. Update Display and Tick Clock
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
