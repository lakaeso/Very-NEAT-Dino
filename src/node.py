import pygame
import random
from utils import *
from enum import Enum
from copy import deepcopy

NODE_NUMBER = 0
starting_nodes = []

class NodeType(Enum):
    SENSOR = 1
    OUTPUT = 2
    HIDDEN = 3

class Node:
    node_type: NodeType
    value: float
    rect: pygame.Rect
    id: int

    def __init__(self, node_type: NodeType, rect: pygame.Rect | None = None):
        global NODE_NUMBER
        self.node_type = node_type
        self.value = 0
        self.id = NODE_NUMBER
        NODE_NUMBER += 1

        if rect is None:
            rect = pygame.Rect(
                NETWORK_DISPLAY_RECT.x + random.randint(0, NETWORK_DISPLAY_RECT.width),
                NETWORK_DISPLAY_RECT.y + random.randint(0, NETWORK_DISPLAY_RECT.height),
                HIDDEN_AND_OUTPUT_NODE_SIZE,
                HIDDEN_AND_OUTPUT_NODE_SIZE
            )
        self.rect = rect

    def __eq__(self, other: 'Node'):
        return self.id == other.id
    
    def __gt__(self, other: 'Node'):
        return self.id > other.id
    
    def __hash__(self):
        return self.id
    
    def __deepcopy__(self, memo):
        return self

    def get_starting_nodes():
        if len(starting_nodes):
            # deepcopy ensures values can be different, while they share the same NODE_NUMBER number and rect
            return deepcopy(starting_nodes)

        w_s = MINI_DISPLAY_RECT.width//NUM_COLS
        h_s = MINI_DISPLAY_RECT.height//NUM_ROWS

        # init input nodes
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                r_s = pygame.Rect(
                    MINI_DISPLAY_RECT.x + j * w_s, 
                    MINI_DISPLAY_RECT.y + i * h_s, 
                    w_s, 
                    h_s
                )
                starting_nodes.append(Node(NodeType.SENSOR, r_s))
        
        # init output nodes
        starting_nodes.append(Node(NodeType.OUTPUT, pygame.Rect(
            NETWORK_DISPLAY_RECT.x + MINI_DISPLAY_RECT.w, 
            NETWORK_DISPLAY_RECT.y + MINI_DISPLAY_RECT.h // 3, 
            HIDDEN_AND_OUTPUT_NODE_SIZE, 
            HIDDEN_AND_OUTPUT_NODE_SIZE
        )))
        starting_nodes.append(Node(NodeType.OUTPUT, pygame.Rect(
            NETWORK_DISPLAY_RECT.x + MINI_DISPLAY_RECT.w, 
            NETWORK_DISPLAY_RECT.y + MINI_DISPLAY_RECT.h // 3 * 2, 
            HIDDEN_AND_OUTPUT_NODE_SIZE, 
            HIDDEN_AND_OUTPUT_NODE_SIZE
        )))

        return starting_nodes
