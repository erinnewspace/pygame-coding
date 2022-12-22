# module: airplane_object


import pygame

#class : GameObject
class GameObject :    

    # object position
    center_below = 0 
    center_upper = 1

    def __init__(self, screen) :
        self.screen = screen
        self.width = 0
        self.height = 0

    def load_image(self, path) : # image loading
        self.image = pygame.image.load(path)

    def set_size(self, w, h) :
        self.width = w
        self.height = h
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def set_position(self, position) :
        
        if position == GameObject.center_below :
            self.x = self.screen.get_size()[0]/2 - self.width/2
            self.y = self.screen.get_size()[1] - self.height
        elif position == GameObject.center_upper :
            self.x = self.screen.get_size()[0]/2 - self.width/2
            self.y = 0
                
    def show(self) :        
        self.screen.blit(self.image, (self.x,self.y))