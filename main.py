"""
File name: main.py
Author: River Stahley
Created: 2025-04-15
Version: 1.0
Description: This script performs a specific task.
"""

import pygame
import os
import random
from pygame import mixer
from classes.powerup import PowerUp
from classes.paddle import Paddle
from classes.ball import Ball
from classes.block import Block

# Initialize the pygame library and the mixer module
pygame.init()
mixer.init()

# Declare constants
WIDTH, HEIGHT = 1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Breaker")
ICON = pygame.image.load("images/icon.png")
FONT = pygame.font.SysFont("comicsans", 30)
PADDLE_VELOCITY, PADDLE_HEIGHT, PADDLE_WIDTH = 15, 20, 150
PADDLE_X, PADDLE_Y = 850, 850
BALL_RADIUS = 10
BALL_VELOCITY = [5, 5] 
BLOCK_WIDTH = 70
BLOCK_HEIGHT = 35
HORIZONTAL_GAP, VERTICAL_GAP = 10, 10
MIN_ROWS, MAX_ROWS = 4, 6
MIN_COLS, MAX_COLS = 8, 10
EXTRA_LIFE = 20000

# Load the title screen image and set the icon
def title_screen():
    pygame.display.set_icon(ICON)
    start_screen = pygame.image.load("images/title_screen.jpg")
    title_screen = pygame.transform.scale(start_screen, (WIDTH, HEIGHT))

    # Load title screen music
    title_screen_music = mixer.Sound("audio/music/title_screen.mp3")
    title_screen_music.set_volume(0.2)

    while True:
        #Display the title screen image
        WINDOW.blit(title_screen, (0, 0))

        start_game = FONT.render("Press Enter to Start", 1, (255, 255, 255))
        start_game_position = start_game.get_rect(centerx=WINDOW.get_rect().centerx, bottom=HEIGHT - 20)  # Position at the bottom
        WINDOW.blit(start_game, start_game_position)

        # Update the display to show the title screen
        pygame.display.update()

        title_screen_music.play()  # Play the title screen music in a loop 

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Exit the game if the window is closed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                title_screen_music.stop()
                return  # Exit the title screen loop to start the game

def display(score, lives, stage, background):
    # Display background
    WINDOW.blit(background, (0, 0))

    # Render the score, lives, high score and stage on the window
    score_text = FONT.render(f"Score: {(score)}", 1, (255, 255, 255))
    score_position = score_text.get_rect()
    score_position.topleft = ((0, 10))
    lives_text = FONT.render(f"Lives: {(lives)}", 1, (255, 255, 255))
    lives_position = lives_text.get_rect()
    lives_position.topright = ((WIDTH, 10))
    high_score_text = FONT.render(f"High Score: {(load_high_score())}", 1, (255, 255, 255))
    high_score_position = high_score_text.get_rect(centerx=WINDOW.get_rect().centerx, top=10)
    stage_text = FONT.render(f"Stage: {(stage)}", 1, (255, 255, 255))
    stage_position = stage_text.get_rect()
    stage_position.bottomright = ((WIDTH, HEIGHT - 10))

    # Display the score, lives, high score and stage on the window
    WINDOW.blit(score_text, (score_position))
    WINDOW.blit(lives_text, lives_position)
    WINDOW.blit(high_score_text, high_score_position)
    WINDOW.blit(stage_text, stage_position)

# Load high score from file
def load_high_score():
    if os.path.exists("data/high_score.txt"):
       with open("data/high_score.txt", "r") as file:
           num = file.read()
           return int(num) if num else 0

# Save high score to file
def save_high_score(score):
    with open("data/high_score.txt", "w") as file:
        file.write(str(score))

# Display game over screen
def game_over(score):
    while True:
        # Load the game over image
        game_over_image = pygame.image.load("images/game_over.jpg")
        game_over_image = pygame.transform.scale(game_over_image, (WIDTH, HEIGHT))
        WINDOW.blit(game_over_image, (0, 0))

        # Render the game over text
        retry_text = FONT.render("Press Enter to Retry", 1, (255, 255, 255))
        exit_text = FONT.render("Press Escape to Exit", 1, (255, 255, 255))
        score_text = FONT.render(f"Score: {(score)}", 1, (255, 255, 255))
        
        # Position the text
        retry_game_position = retry_text.get_rect(centerx=WINDOW.get_rect().centerx, bottom=HEIGHT - 20)
        exit_game_position = exit_text.get_rect(centerx=WINDOW.get_rect().centerx, bottom=HEIGHT - 60)
        score_text_position = score_text.get_rect(centerx=WINDOW.get_rect().centerx, top=10)

        # Display the text on the window
        WINDOW.blit(retry_text, retry_game_position)
        WINDOW.blit(exit_text, exit_game_position)
        WINDOW.blit(score_text, score_text_position)
        
        # Update the display to show the game over screen
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Retry the game
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def main():
    # Game loop
    run = True

    # Create a ball and paddle
    ball = Ball("sprites/ball.png", radius=BALL_RADIUS, velocity=BALL_VELOCITY)
    paddle = Paddle("sprites/paddle.png", PADDLE_X, PADDLE_Y, PADDLE_VELOCITY, width=PADDLE_WIDTH, height=PADDLE_HEIGHT)
   
    # Initialize clock to control the frame rate
    clock = pygame.time.Clock()

    # Add a flag to track if the game is waiting for the ball to launch
    waiting_for_launch = True

    # Number of rows and columns
    num_rows = random.randint(MIN_ROWS, MAX_ROWS)
    num_cols = random.randint(MIN_COLS, MAX_COLS)

    # Calculate total grid dimensions
    total_width = (num_cols * BLOCK_WIDTH) + ((num_cols - 1) * HORIZONTAL_GAP)
    total_height = (num_rows * BLOCK_HEIGHT) + ((num_rows - 1) * VERTICAL_GAP)

    # Calculate offsets to center the grid
    x_offset = (WIDTH - total_width) // 2
    y_offset = (HEIGHT - total_height) // 2 - 250

    # Initialize the backgrounds
    background_paths = ["images/background #1.jpg", "images/background #2.jpg", "images/background #3.jpg",
                    "images/background #4.jpg", "images/background #5.jpg"]
    backgrounds = [pygame.transform.scale(pygame.image.load(path).convert(), (WIDTH, HEIGHT)) for path in background_paths]
    current_background = random.choice(backgrounds)  # Randomly select a background image

    # Initialize the blocks
    block_images = ["sprites/blocks/+50.png", "sprites/blocks/+100.png", "sprites/blocks/+250.png", "sprites/blocks/+500.png", 
                    "sprites/blocks/block1.png", "sprites/blocks/block2.png", "sprites/blocks/block3.png", "sprites/blocks/block4.png", 
                    "sprites/blocks/block5.png", "sprites/blocks/block6.png", "sprites/blocks/block7.png", "sprites/blocks/block8.png", 
                    "sprites/blocks/block9.png", "sprites/blocks/block10.png", "sprites/blocks/block11.png", "sprites/blocks/block12.png", 
                    "sprites/blocks/block13.png", "sprites/blocks/block14.png", "sprites/blocks/block15.png", "sprites/blocks/block16.png", 
                    "sprites/blocks/block17.png", "sprites/blocks/block18.png", "sprites/blocks/block19.png", "sprites/blocks/block20.png"]
    block_scores = [50, 100, 250, 500, 30, 30, 40, 40, 50, 50, 60, 60, 70, 70, 80, 80, 90, 90, 100, 100, 110, 110, 120, 120]
    blocks = Block.create_blocks(min_rows=num_rows, max_rows=num_rows, min_cols=num_cols, max_cols=num_cols,
                                 block_width=BLOCK_WIDTH, block_height=BLOCK_HEIGHT, images=block_images, scores=block_scores, 
                                 x_offset=x_offset, y_offset=y_offset, horizontal_gap=HORIZONTAL_GAP, vertical_gap=VERTICAL_GAP)
    
    # Initialize the power-ups
    power_ups = [PowerUp("sprites/power_ups/extra_life.jpeg", 50, 50, velocity=(0,6)), 
             PowerUp("sprites/power_ups/slow_ball.png", 50, 50, velocity=(0,6)),
             PowerUp("sprites/power_ups/fast_ball.png", 50, 50, velocity=(0,6)),
             PowerUp("sprites/power_ups/wide_paddle.png", 50, 50, velocity=(0,6))]
    
    # Load sound effects
    block_destroyed_sound = mixer.Sound("audio/sound effects/block_destroyed.mp3")
    lose_life_sound = mixer.Sound("audio/sound effects/lose_life.mp3")
    paddle_hit_sound = mixer.Sound("audio/sound effects/paddle_hit.mp3")
    power_up_sound = mixer.Sound("audio/sound effects/power_up.mp3")
    game_over_sound = mixer.Sound("audio/sound effects/game_over.mp3")
    stage_complete_sound = mixer.Sound("audio/sound effects/stage_complete.mp3")
    high_score_sound = mixer.Sound("audio/sound effects/high_score.mp3")

    # Load background music
    tracks = ["audio/music/track #1.mp3", "audio/music/track #2.mp3", "audio/music/track #3.mp3", 
              "audio/music/track #4.mp3", "audio/music/track #5.mp3"]
    background_music = mixer.Sound(random.choice(tracks))  
    background_music.set_volume(0.2)  

    # Set the volume for the sound effects and music
    block_destroyed_sound.set_volume(0.5)
    lose_life_sound.set_volume(0.5)
    paddle_hit_sound.set_volume(0.5)
    power_up_sound.set_volume(0.5)
    game_over_sound.set_volume(0.5)                                       
    stage_complete_sound.set_volume(0.5)                         
    high_score_sound.set_volume(0.5)
                                     
    # Initialize variables
    score = 0
    lives = 5
    original_velocity = ball.velocity.copy() 
    high_score = load_high_score()
    stage = 1
    blocks_destroyed = 0  
    spawn_power_up = random.randint(5, 10)  
    powerUp_displayed = False  
    active_power_up = None  
    waiting_for_launch = True  
    show_launch_message = True  

    # call the title screen function to display the title screen

    title_screen()

    background_music.play(loops=-1)  # Play background music in a loop

    while run:
        clock.tick(60)

        #Handle events in the game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and waiting_for_launch:
                    # Launch the ball when Enter is pressed
                    ball.velocity = BALL_VELOCITY
                    waiting_for_launch = False
                    show_launch_message = False  # Hide the launch message
        
        # Check for key presses to move the paddle
        controls = pygame.key.get_pressed()

        # Move the paddle
        paddle.move(controls, WIDTH)

        # If waiting for launch, position the ball on the paddle
        if waiting_for_launch:
            ball.rect.x = paddle.rect.centerx - ball.rect.width // 2
            ball.rect.y = paddle.rect.top - ball.rect.height
        
        # Check for collisions with the window boundaries
        if ball.check_collision(WIDTH, HEIGHT):
            lives -= 1  
            lose_life_sound.play()

            # Clear the screen and update the display to show lives as 0
            display(score, lives, stage, current_background)
            paddle.draw(WINDOW)
            ball.draw(WINDOW)
            blocks.draw(WINDOW)
            pygame.display.update()

            # Pause the game for a short duration
            pygame.time.delay(1000)  

            # Deactivate the currently active power-up
            if active_power_up == power_ups[1]:  
                ball.velocity = original_velocity.copy()
            elif active_power_up == power_ups[2]:  
                ball.velocity = original_velocity.copy()
            elif active_power_up == power_ups[3]:  
                paddle.image = pygame.transform.scale(paddle.image, (paddle.original_width, paddle.rect.height))
                paddle.rect = paddle.image.get_rect(center=paddle.rect.center)

            active_power_up = None
            powerUp_displayed = False

            # Reset the ball position and velocity
            ball.rect.x = paddle.rect.centerx - ball.rect.width // 2
            ball.rect.y = paddle.rect.top - ball.rect.height
            ball.velocity = [0, 0] 
            waiting_for_launch = True

            # End the game if lives reach 0
            if lives <= 0:
                pygame.time.delay(100)
                background_music.stop()  
                game_over_sound.play(loops=-1)  
                retry = game_over(score)  
                if retry:
                    game_over_sound.stop()  
                    main()  
                else:
                    run = False
                    break 
        
        #Call the display function to update the window
        display(score, lives, stage, current_background)
        paddle.draw(WINDOW)
        ball.draw(WINDOW)   
        blocks.draw(WINDOW)

        # Render the "Press Enter to Launch Ball" message if waiting for launch
        if waiting_for_launch and show_launch_message:
            launch_ball = FONT.render("Press Enter to Launch Ball", True, (255, 255, 255))
            game_start = launch_ball.get_rect(center=(WIDTH // 2, HEIGHT - 50))  
            WINDOW.blit(launch_ball, game_start)
        
        # Move the ball only if it's not waiting for launch
        if not waiting_for_launch:
            ball.move()

        if ball.rect.colliderect(paddle.rect):
            ball.velocity[1] *= -1
            
            # Calculate the collision point on the paddle
            paddle_center = paddle.rect.centerx
            ball_center = ball.rect.centerx
            collision_offset = ball_center - paddle_center

            # Adjust the horizontal velocity based on the collision offset
            max_offset = paddle.rect.width // 2  
            ball.velocity[0] = (collision_offset / max_offset) * 5  

            # Ensure the ball's horizontal velocity is not zero
            if ball.velocity[0] == 0:
                ball.velocity[0] = random.choice([-1, 1]) * 2  

            paddle_hit_sound.play()  # Play sound effect on paddle hit

        for block in blocks:
            if ball.rect.colliderect(block.rect):
                block_destroyed_sound.play()
                blocks.remove(block)
                ball.velocity[1] *= -1
                score += block.score  # Add the score of the destroyed block to the total score
                blocks_destroyed += 1
                break
        
        if blocks_destroyed >= spawn_power_up and not powerUp_displayed:
            power_up = random.choice(power_ups)  # Randomly select a power-up
            random_x = random.randint(50, WIDTH - 50)
            random_y = random.randint(50, HEIGHT // 2)
            power_up.set_position(random_x, random_y)
            powerUp_displayed = True

            # Reset the threshold for the next power-up
            spawn_power_up = blocks_destroyed + random.randint(5, 10)  # Add a random number to the current count

        if powerUp_displayed:
            power_up.update()
            WINDOW.blit(power_up.image, power_up.rect)

            # Check if the power-up collides with the paddle
            if power_up.rect.colliderect(paddle):
                powerUp_displayed = False  # Remove the power-up after it is collected

                power_up_sound.play()  # Play sound effect on power-up collection

                # Deactivate the currently active power-up
                if active_power_up == power_ups[1]:  # Reset slow ball power-up
                    ball.velocity = original_velocity.copy()
                elif active_power_up == power_ups[2]:  # Reset fast paddle power-up
                    ball.velocity = original_velocity.copy()
                elif active_power_up == power_ups[3]:  # Reset wide paddle power-up
                    paddle.image = pygame.transform.scale(paddle.image, (paddle.original_width, paddle.rect.height))
                    paddle.rect = paddle.image.get_rect(center=paddle.rect.center)

                # Activate the new power-up
                active_power_up = power_up
                if power_up == power_ups[0]:  # Extra life power-up
                    lives += 1
                    score += 150
                elif power_up == power_ups[1]:  # Slow ball power-up
                    ball.velocity[0] *= 0.8
                    ball.velocity[1] *= 0.8
                    score += 150
                elif power_up == power_ups[2]:  # Fast ball power-up
                    ball.velocity[0] *= 2
                    ball.velocity[1] *= 2
                    score += 150
                elif power_up == power_ups[3]:  # Wide paddle power-up
                    original_width = paddle.rect.width
                    paddle.image = pygame.transform.scale(paddle.image, (paddle.rect.width * 2, paddle.rect.height))
                    paddle.rect = paddle.image.get_rect(center=paddle.rect.center)
                    paddle.original_width = original_width
                    score += 150

        # advance to next stage      
        if not blocks:
            stage += 1
            stage_complete_sound.play()  # Play stage complete sound effect

            current_background = random.choice(backgrounds)  # Randomly select a new background image

            ball.velocity[0] *= 1.5  
            ball.velocity[1] *= 1.5

            # Regenerate the blocks for the next stage
            num_rows = random.randint(MIN_ROWS, MAX_ROWS)
            num_cols = random.randint(MIN_COLS, MAX_COLS)
            blocks = Block.create_blocks(
                min_rows=num_rows,
                max_rows=num_rows,
                min_cols=num_cols,
                max_cols=num_cols,
                block_width=BLOCK_WIDTH,
                block_height=BLOCK_HEIGHT,
                images=block_images,
                scores=block_scores,
                x_offset=x_offset,
                y_offset=y_offset,
                horizontal_gap=HORIZONTAL_GAP,
                vertical_gap=VERTICAL_GAP
            )
            blocks.draw(WINDOW)
            pygame.time.delay(1000) 
               
        if score >= EXTRA_LIFE and score % EXTRA_LIFE == 0:
            lives += 1  # Increase lives by 1 for every 20000 points
            power_up_sound.play()  # Play sound effect for extra life
        
        if score > high_score:
            high_score = score
            high_score_sound.play()
        
        # Save the high score if it changes    
        save_high_score(high_score)

        #Update the display to show the changes
        pygame.display.update()
        
    #end the game loop
    pygame.quit()

#call the main function to start the game
if __name__ == "__main__":
    main()