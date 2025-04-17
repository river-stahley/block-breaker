import pygame
import random

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, images, scores):
        super().__init__()
        self.images = [pygame.image.load(img).convert_alpha() for img in images]
        self.image_index = random.randint(0, len(self.images) - 1)
        self.image = pygame.transform.scale(self.images[self.image_index], (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Assign a score based on the image index
        self.score = scores[self.image_index]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    @staticmethod
    def create_blocks(min_rows, max_rows, min_cols, max_cols, block_width, block_height, images, scores, x_offset, y_offset, horizontal_gap, vertical_gap):
        blocks_group = pygame.sprite.Group()
        num_rows = random.randint(min_rows, max_rows)
        num_cols = random.randint(min_cols, max_cols)

        for row in range(num_rows):
            for col in range(num_cols):
                x = x_offset + col * (block_width + horizontal_gap)
                y = y_offset + row * (block_height + vertical_gap)
                block = Block(x, y, block_width, block_height, images, scores)
                blocks_group.add(block)

        return blocks_group