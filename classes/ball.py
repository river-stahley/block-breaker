import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, image_path, radius, velocity):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))  
        self.rect = self.image.get_rect()  
        self.velocity = velocity
        self.radius = radius

    def move(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
    
    def check_collision(self, screen_width, screen_height):
       
        # Reverse horizontal direction if the ball hits the left or right edge
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.velocity[0] = -self.velocity[0]

        # Reverse vertical direction if the ball hits the top or bottom edge
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.velocity[1] = -self.velocity[1]

        # Check if the ball falls below the screen
        if self.rect.bottom >= screen_height:
            return True  # Ball has fallen below the screen

        return False  # Ball is still in play
    
    def draw(self, window):
        window.blit(self.image, self.rect)