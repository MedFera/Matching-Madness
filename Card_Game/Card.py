import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, back_image, front_image, initial_x, initial_y):
        super().__init__()

        self.name = front_image
        self.match_found = False
        
        self.front_face = pygame.image.load(front_image)
        self.back_face = pygame.image.load(back_image)

        # Load the sprite's image
        self.image = self.back_face
        
        #Card state of flipped
        self.is_flipped = False
        
        # Set the sprite's rect (position and size)
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y

        # Additional attributes and behaviors can be added here
    def update(self):
        
        #NEED TO GET FLIP ANIMATION
        if self.is_flipped == True:
            self.image = self.front_face
        
        elif self.is_flipped == False:
            self.image = self.back_face
        
        else:
            print("Flipping error")

    def draw(self, screen):
        # Blit the sprite onto the screen
        screen.blit(self.image, self.rect)