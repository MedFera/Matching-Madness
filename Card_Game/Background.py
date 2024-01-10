import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_paths, initial_x, initial_y):
        super().__init__()

        # Load all frames of the animation
        self.frames = []
        for image_path in image_paths:
            self.frames.append(pygame.image.load(image_path))

       # Set the sprite's rect (position and size)
        self.rect = self.frames[0].get_rect()
        self.rect.x = initial_x
        self.rect.y = initial_y

        # Animation properties
        self.frame_index = 0  # Current frame index
        self.animation_speed = 10  # How many frames before new picture is put into frame
        self.frame_timer = 0  # Timer to control frame switching
        
        # Additional attributes and behaviors can be added here
    def update(self):
        self.frame_timer += 1

        # If the frame timer exceeds the animation speed, switch to the next frame
        if self.frame_timer >= self.animation_speed:
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.frame_index = 0  # Reset to the first frame
            self.frame_timer = 0  # Reset the frame timer

        # Set the current image based on the frame index
        self.image = self.frames[self.frame_index]

    def draw(self, screen):
        # Blit the sprite onto the screen
        screen.blit(self.image, self.rect)