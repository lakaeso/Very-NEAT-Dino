import pygame
from utils import *
from genome import Genome

class ReceptiveField:
    
    rects_list: list[pygame.Rect]

    def __init__(self):
        self.rects_list = []
        w = SCREEN_WIDTH//NUM_COLS
        h = SCREEN_HEIGHT//NUM_ROWS

        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                r = pygame.Rect(
                    j * w, 
                    i * h, 
                    w, 
                    h
                )
                self.rects_list.append(r)

    def forward(self, genome: Genome, obstacles, player):
        # transform input
        network_inputs = []

        for r in self.rects_list:
            colision_detected = -1
            for obstacle in obstacles:
                if r.collidepoint(obstacle.rect.center):
                    colision_detected = 1
                    break
            network_inputs.append(colision_detected)
        
        # fwd pass
        key_up_value, key_down_value = genome.forward_pass(network_inputs)

        key_dict = {pygame.K_UP: False, pygame.K_DOWN: False}
        
        if key_up_value > 0:
            key_dict[pygame.K_UP] = True
        
        if key_down_value > 0:
           key_dict[pygame.K_DOWN] = True

        player.update(key_dict)
