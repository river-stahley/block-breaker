import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, velocity=(0, 0)):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.velocity = velocity
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Update sprite position or state if needed
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]