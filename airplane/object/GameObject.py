import pygame

# GameObejct class
class GameObject :    
    center_below = 0
    
    def __init__(self) :
        self.x = 0
        self.y = 0        

    def load_image(self, path) :
        if path[-3:] == 'png':
            self.image = pygame.image.load(path).convert_alpha()
        else:
            self.image = pygame.image.load(path)

    def set_size(self, w, h) :
        self.image = pygame.transform.scale(self.image, (w, h))

    def set_position(self, position) :
        image_size = self.image.get_size()
        screen_size = pygame.display.get_surface().get_size() # screen size       
        
        if position == GameObject.center_below :
            self.x = round(screen_size[0]/2 - image_size[0]/2) # center
            self.y = round(screen_size[1]- image_size[1]) # below    
        
    def show(self) :
        pygame.display.get_surface().blit(self.image, (self.x, self.y))   