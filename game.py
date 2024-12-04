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
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        
    def draw_object(self, screen: pygame.surface, x: float, y: float) -> None:
        screen.blit(self.surface, (x, y))
        self.x = x
        self.y = y    
        self.rect.topleft = (x, y)
        
    def move_rect(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.rect.topleft = (x, y)
        
    def collides_with(self, other: 'GameObject') -> bool:
        return self.rect.colliderect(other.rect)
        
        
class Player(GameObject):
    def __init__(self) -> None:
        super().__init__(x_init=300, y_init=200, width=20, height=20, color=(255, 255, 255))
        
        self.gravity: float = 20
        self.acceleration: float = self.gravity
        self.velocity: float = 0
        self.jumpforce: float  = -7.5
        
        self.score: int = 0
        self.justScored: bool = False
        
    def draw_player(self, screen: pygame.Surface) -> None:
        self.draw_object(screen, self.x, self.y)    
    
    def animate_player(self, screen: pygame.Surface, delta_time: float) -> None:
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.velocity = self.jumpforce
        
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
    
    def check_score(self, obj: GameObject) -> bool:
        collided: bool = self.collides_with(obj)
        if collided and not self.justScored:
            self.score += 1
            self.justScored = True
            return True
        elif not collided:
            self.justScored = False
        return False

class Gate():
    def __init__(self, speed: float = 1) -> None:        
        self.speed = speed
        self.width: float = 150
        self.height: float = 500
         
        self.gate_up: GameObject = GameObject(700, -self.height + 200, self.width, self.height, (0, 255, 0))
        self.gate_down: GameObject = GameObject(700, 400, self.width, self.height, (0, 255, 0))
        
        self.score_gate: GameObject = GameObject(700 + self.width/2, 0, self.width/10, self.height, (0, 0, 0))
        
    def draw_gate(self, screen: pygame.Surface) -> None:
        self.gate_up.draw_object(screen, self.gate_up.x, self.gate_up.y)
        self.gate_down.draw_object(screen, self.gate_down.x, self.gate_down.y)
        self.score_gate.move_rect(self.score_gate.x, self.score_gate.y)
    
    def animate_gate(self, screen: pygame.Surface) -> None:        
        if (self.gate_up.x < -150 and self.gate_down.x < -150):
            x_up_new = 800 
            x_down_new = 800
            x_score_new = 800
            
            y_random = random.randint(-200, 200)
            y_up_new = -self.height + 200 + y_random
            y_down_new = 400 + y_random
            y_score_new = 0
            
        else:
            x_up_new = self.gate_up.x - 1 * self.speed
            x_down_new = self.gate_down.x -1 * self.speed
            x_score_new = self.score_gate.x -1 * self.speed
            
            y_up_new = self.gate_up.y
            y_down_new = self.gate_down.y
            y_score_new = self.score_gate.y
            
        self.gate_up.draw_object(screen, x_up_new, y_up_new)
        self.gate_down.draw_object(screen, x_down_new, y_down_new)
        self.score_gate.move_rect(x_score_new, y_score_new)
        
    def get_gates(self) -> List[GameObject]:
        return [self.gate_up, self.gate_down]
        
    def get_score_gate(self) -> GameObject:
        return self.score_gate
        
if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    shutDownFlag = False
    
    clock: pygame.time.Clock = pygame.time.Clock()
    screen: pygame.Surface = pygame.display.set_mode((800, 600))
    font: pygame.font.Font = pygame.font.SysFont("Arial", 30)
    FPS: int = 60
    
    while not shutDownFlag:
        gate = Gate(speed=5)
        player = Player()
        gate.draw_gate(screen)
        player.draw_player(screen)

        restartFlag = False
        
        while not restartFlag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shutDownFlag = True
                    restartFlag = True
            
            delta_time = clock.tick(FPS) / 1000
                    
            screen.fill((0, 0, 0))
            player.animate_player(screen, delta_time)
            gate.animate_gate(screen)
            text_surface = font.render(str(player.score), True, (255, 255, 255))
            screen.blit(text_surface, (400, 20))
            
            player.check_score(gate.get_score_gate())    
            restartFlag = player.is_dead(gate.get_gates())
                        
            pygame.display.flip()
            
        del gate
        del player