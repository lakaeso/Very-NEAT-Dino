from node import Node
import random
from utils import *

EPOCH_INNOVATIONS: list['Connection'] = []

class Connection:
    input: Node
    output: Node
    weight: float
    is_enabled: bool
    innovation_number: int

    def __init__(self, input: Node, output: Node, weight: float | None = None):
        global INNOVATION_NUMBER, EPOCH_INNOVATIONS
        self.input = input
        self.output = output
        match = None
        for c in EPOCH_INNOVATIONS:
            if self.input == c.input and self.output == c.output:
                match = c.innovation_number
        
        if match is None:
            INNOVATION_NUMBER += 1
            self.innovation_number = INNOVATION_NUMBER
            EPOCH_INNOVATIONS.append(self)
        else:
            self.innovation_number = match
        self.is_enabled = True
        self.weight = weight if weight is not None else random.choice([-1, 1])  


    def __gt__(self, other: 'Connection'):
        return self.innovation_number > other.innovation_number
                
    def __eq__(self, other: 'Connection'):
        if self.innovation_number == other.innovation_number:
            assert (self.input == other.input and self.output == other.output)
            return True
        else:
            return False

    def __str__(self):
        return f"{self.input.id}=>{self.output.id}"