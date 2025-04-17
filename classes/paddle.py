import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, velocity, width=150, height=20):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect() 
        self.rect.topleft = (x, y)
        self.velocity = velocity 
        self.multiplier = 1  # Multiplier for paddle speed (used for power-ups)

    def move(self, controls, screen_width):
        if controls[pygame.K_LEFT] and self.rect.left - self.velocity >= 0:
            self.rect.x -= self.velocity 
        if controls[pygame.K_RIGHT] and self.rect.right + self.velocity <= screen_width:
            self.rect.x += self.velocity 
    
    def draw(self, window):
        window.blit(self.image, self.rect)