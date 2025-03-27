import pygame
import os

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
NUM_ROWS = 5
NUM_COLS = 13
MINI_DISPLAY_RECT = pygame.Rect(50, 50, 200, 200) # this will be divided in NUM_ROWS x NUM_COLS
NETWORK_DISPLAY_RECT = pygame.Rect(250, 50, 200, 200)

HIDDEN_AND_OUTPUT_NODE_SIZE = 20

INNOVATION_NUMBER = 0
EPOCH = 0

GAME_SPEED = 30
ELITISM_RATE = 0.1

ADD_NODE_MUTATION_RATE = 0.2
ADD_CONN_MUTATION_RATE = 0.2
CHANGE_CONN_MUTATION_RATE = 0
ENABLE_CONN_MUTATION_RATE = 0

DELTA_THRESH = 0.3
POPULATION_SIZE = 100
GENERATIONS = 100

RANDOM_SEED = 42

c1, c2, c3 = 1, 1, 0.4

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))