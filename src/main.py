import pygame
from utils import *
from genome import Genome
from game import play_round
from genome import *
from species import *

pygame.init()

def main(): 
    population = [Genome() for _ in range(POPULATION_SIZE)]

    speciate(population=population)

    for gen in range(GENERATIONS):
        print(f"\nGeneration {gen}")
        
        population = select_and_reproduce(population)
        speciate(population=population)

        for genome in population:
            genome.fitness = play_round(genome)

    print("Evolution complete!")

if __name__ == "__main__":
    main()
