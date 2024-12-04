import pygame
from typing import List, Optional
import random    

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x_init: float, y_init: float, width: float, height: float, color: pygame.Color) -> None:
        self.x, self.y = x_init, y_init
        self.width = width
        self.height = height
        self.color = color
        
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        
    def draw_object(self, screen: pygame.surface, x: float, y: float) -> None:
        screen.blit(self.surface, (x, y))
        self.x = x
        self.y = y    
        
    def collides_with(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)
        
        
class Player(GameObject):
    def __init__(self) -> None:
        super().__init__(x_init=300, y_init=200, width=50, height=50, color=(255, 255, 255))
        
        self.gravity = 9.81
        self.acceleration = self.gravity
        self.velocity = 0
        
    def draw_player(self, screen: pygame.Surface) -> None:
        self.draw_object(screen, self.x, self.y)    
    
    def animate_player(self, screen: pygame.Surface, delta_time: float) -> None:
        self.velocity += self.acceleration * delta_time
        self.y += self.velocity
        
        self.draw_object(screen, self.x, self.y)
        
    def is_dead(self, objects: Optional[List[GameObject]]=None) -> bool:
        if self.y > 600:
            return True

        if objects:
            for obj in objects:
                if self.collides_with(obj):
                    return True
        
        return False
        

class Gate():
    def __init__(self, speed: float = 1) -> None:        
        self.speed = speed
        self.width = 150
        self.height = 500
        
        self.gate_up: GameObject = GameObject(500, -self.height + 200, self.width, self.height, (0, 255, 0))
        self.gate_down: GameObject = GameObject(500, 400, self.width, self.height, (0, 255, 0))
        
        
    def draw_gate(self, screen: pygame.Surface) -> None:
        self.gate_up.draw_object(screen, self.gate_up.x, self.gate_up.y)
        self.gate_down.draw_object(screen, self.gate_down.x, self.gate_down.y)
    
    def animate_gate(self, screen: pygame.Surface) -> None:        
        if (self.gate_up.x < -150 and self.gate_down.x < -150):
            x_up_new = 800 
            x_down_new = 800
            
            y_random = random.randint(-200, 200)
            y_up_new = -self.height + 200 + y_random
            y_down_new = 400 + y_random
            
        else:
            x_up_new = self.gate_up.x - 1 * self.speed
            x_down_new = self.gate_down.x -1 * self.speed
            
            y_up_new = self.gate_up.y
            y_down_new = self.gate_down.y
            
        self.gate_up.draw_object(screen, x_up_new, y_up_new)
        self.gate_down.draw_object(screen, x_down_new, y_down_new)
        
    def get_gates(self) -> List[GameObject]:
        return [self.gate_up, self.gate_down]
        
        
if __name__ == "__main__":
    pygame.init()
    gate = Gate(speed=5)
    player = Player()
    
    shutDownFlag = False
    FPS = 60
    screen = pygame.display.set_mode((800, 600))
    gate.draw_gate(screen)
    player.draw_player(screen)
    clock = pygame.time.Clock()

    while not shutDownFlag:
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                shutDownFlag = True
        screen.fill((0, 0, 0))
        player.animate_player(screen, delta_time)
        gate.animate_gate(screen)
        if (player.is_dead(gate.get_gates())):
            shutDownFlag = True
        pygame.display.flip()