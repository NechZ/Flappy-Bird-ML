import neat.config
import neat.genome
import neat.statistics
import pygame
from typing import List, Optional, Tuple
import random
import neat
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x_init: float, y_init: float, width: float, 
                 height: float, color: pygame.Color) -> None:
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
        super().__init__(x_init=300, y_init=200, width=20, height=20, 
                         color=(255, 255, 255))
        
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
        
    def is_dead(self, objects: Optional[List[GameObject]]=None) -> int:
        if self.y > 600 or self.y < 0:
            return 0

        if objects:
            for obj in objects:
                if self.collides_with(obj):
                    return 1
        
        return -1
    
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
         
        self.gate_up: GameObject = GameObject(700, -self.height + 200,
                                              self.width, self.height, (0, 255, 0))
        self.gate_down: GameObject = GameObject(700, 400, self.width, 
                                                self.height, (0, 255, 0))
        
        self.score_gate: GameObject = GameObject(700 + self.width/2, 0, 
                                                 self.width/10, self.height, (0, 0, 0))
        
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
    
    def get_top_left(self) -> Tuple[float, float]:
        return (self.gate_up.x, self.gate_up.y - self.height)
    def get_bottom_right(self) -> Tuple[float, float]:
        return (self.gate_up.x + self.width, self.gate_down.y)
        
class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.shutDownFlag = False
        
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen: pygame.Surface = pygame.display.set_mode((800, 600))
        self.font: pygame.font.Font = pygame.font.SysFont("Arial", 30)
        self.FPS: int = 120
    
    def start_game(self, genomes: List[Tuple[int, neat.genome.DefaultGenome]], 
                   config: neat.config.Config) -> None:
        self.gate = Gate(speed=5)
        self.players: List[Player] = []
        self.nets: List[neat.nn.FeedForwardNetwork] = []
        self.genomes: List[neat.genome.DefaultGenome] = []
        self.shutDownFlag = False
        
        for _, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.nets.append(net)
            self.players.append(Player())
            genome.fitness = 0
            self.genomes.append(genome)
            
        self.gate.draw_gate(self.screen)
        for player in self.players:
            player.draw_player(self.screen)
            
        while not self.shutDownFlag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.shutDownFlag = True
                    pygame.quit()
                    return
                    
            self._refresh_display()
            
            if not self.players:
                break
        
        del self.gate
        del self.players
        del self.nets
        del self.genomes
        print("RESTARTING")
            
    def jump_player(self, player: Player) -> None:
        player.velocity = player.jumpforce
        
    def get_state(self, player: Player) -> dict:
        state = {}
        state["Y_player"] = float(player.y)
        state["V_player"] = float(player.velocity)
        top_left_x, top_left_y =  self.gate.get_top_left()
        bottom_right_x, bottom_right_y = self.gate.get_bottom_right()
        state["Top_left_x"] = float(top_left_x)
        state["Top_left_y"] = float(top_left_y)
        state["Bottom_right_x"] = float(bottom_right_x)
        state["Bottom_right_y"] = float(bottom_right_y)
        
        return state        
                    
    def _refresh_display(self) -> None:
        self.delta_time = self.clock.tick(self.FPS) / 1000
        self.screen.fill((0, 0, 0))
        
        for i, player in enumerate(self.players):
            state = self.get_state(player)
            output = self.nets[i].activate(list(state.values()))
            if output[0] > 0.5:
                self.jump_player(player)           
            
            death_code: int = player.is_dead(self.gate.get_gates())
            
            if death_code in [0, 1]:
                self.genomes[i].fitness -= 2 if death_code == 1 else 1
                self.players.pop(i)
                self.nets.pop(i)
                self.genomes.pop(i)
            
            player.animate_player(self.screen, self.delta_time)
            if player.check_score(self.gate.get_score_gate()):
                self.genomes[i].fitness += 1
            
    
        if self.players:
            max_score = max(player.score for player in self.players)
        else:
            max_score = 0
             
        text_surface = self.font.render(str(max_score), True, (255, 255, 255))
        self.screen.blit(text_surface, (400, 20))
        text_genome_surface = self.font.render(str(len(self.players)), True, (255, 255, 255))
        self.screen.blit(text_genome_surface, (200, 20))
        
        self.gate.animate_gate(self.screen)
        pygame.display.flip()
            
if __name__ == "__main__":
    
    config_path = "./neat_config.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    #population = neat.Checkpointer.restore_checkpoint("")
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats_reporter = neat.StatisticsReporter()
    population.add_reporter(stats_reporter)
    population.add_reporter(neat.Checkpointer(1))
    
    game = Game()
    population.run(game.start_game, 200)
    
    pygame.quit()