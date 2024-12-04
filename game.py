import pygame
from typing import List
import random

pygame.init()

class Position():
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def get_position(self) -> List[float]:
        position = [0, 0]
        position[0] = self.x
        position[1] = self.y
        return position
    
    def set_position(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        

class Gate(pygame.sprite.Sprite):
    def __init__(self, speed: float = 1) -> None:
        super(Gate, self).__init__()
        
        self.speed = speed
        self.width = 150
        self.height = 500
        
        self.surface_up = pygame.Surface((self.width, self.height))
        self.surface_up.fill((0, 255, 0))
        self.rect_up = self.surface_up.get_rect()
        self.position_up = Position()
   
        self.surface_down = pygame.Surface((self.width, self.height))
        self.surface_down.fill((0, 255, 0))
        self.rect_down = self.surface_down.get_rect()
        self.position_down = Position()
        
    def draw_gate(self, screen: pygame.Surface) -> None:
        screen.blit(self.surface_up, (500, -self.height + 200))
        screen.blit(self.surface_down, (500,400))
        
        self.position_up.set_position(500, -self.height + 200)
        self.position_down.set_position(500, 400)
    
    def animate_gate(self, screen: pygame.Surface) -> None:
        
        x_up: int = self.position_up.get_position()[0]
        y_up: int = self.position_up.get_position()[1]
        
        x_down: int = self.position_down.get_position()[0]
        y_down: int = self.position_down.get_position()[1]
        
        if (x_up < -150 and x_down < -150):
            x_up_new = 800 
            x_down_new = 800
            
            y_random = random.randint(-200, 200)
            y_up_new = -self.height + 200 + y_random
            y_down_new = 400 + y_random
            
        else:
            x_up_new = x_up - 1 * self.speed
            x_down_new = x_up -1 * self.speed
            
            y_up_new = y_up
            y_down_new = y_down
        screen.blit(self.surface_up, (x_up_new, y_up_new))
        screen.blit(self.surface_down, (x_down_new, y_down_new))  
        
        self.position_up.set_position(x_up_new, y_up_new)
        self.position_down.set_position(x_down_new, y_down_new)
        
        
if __name__ == "__main__":
    square_1 = Gate(speed=0.5)
    
    shutDownFlag = False
    screen = pygame.display.set_mode((800, 600))
    square_1.draw_gate(screen)

    while not shutDownFlag:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                shutDownFlag = True
        screen.fill((0, 0, 0))
        square_1.animate_gate(screen)
        pygame.display.flip()