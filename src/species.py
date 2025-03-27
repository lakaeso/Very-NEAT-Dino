from genome import *

SPECIES_FROM_LAST_GEN: dict[int, list['Genome']] = {}
SPECIES_NUM = 0

def speciate(population: list['Genome']):
    global SPECIES_FROM_LAST_GEN, SPECIES_NUM

    species: dict[int, list['Genome']] = {}
    for genome in population:
        match_found = False
        for species_num in SPECIES_FROM_LAST_GEN:
            if genome.compatibility_distance(SPECIES_FROM_LAST_GEN[species_num][0]) < DELTA_THRESH:
                species.setdefault(species_num, []).append(genome)
                genome.species = species_num
                genome.delta = genome.compatibility_distance(SPECIES_FROM_LAST_GEN[species_num][0])
                match_found = True
                break
        if not match_found:
            SPECIES_NUM += 1
            species.setdefault(SPECIES_NUM, []).append(genome)
            genome.species = SPECIES_NUM
            genome.delta = 0
            SPECIES_FROM_LAST_GEN.setdefault(SPECIES_NUM, []).append(genome)
        if genome.delta > 3 and genome.delta < 1000: print(genome.delta)

    SPECIES_FROM_LAST_GEN = deepcopy(species)

def select_and_reproduce(population: list['Genome']) -> list['Genome']:
    global EPOCH_INNOVATIONS
    species = deepcopy(SPECIES_FROM_LAST_GEN)

    # Adjust fitness
    for genome in population:
        for id, s in species.items():
            if genome.compatibility_distance(s[0]) < DELTA_THRESH:
                genome.fitness /= len(s)
                genome.species = id
                break

    total_adjusted_fitness = sum([sum([g.fitness for g in s]) for s in species.values()])
    
    new_population = []

    for id, s in species.items():
        offspring_count = round((sum(g.fitness for g in s) / total_adjusted_fitness) * len(population))
        if len(s) == 1:
            s.append(deepcopy(s[0]))

        s.sort(key=lambda g: g.fitness, reverse=True)

        num_elites = max(1, round(ELITISM_RATE * len(s)))
        new_population.extend(deepcopy(s[:num_elites]))

        for _ in range(offspring_count - num_elites):
            parent1, parent2 = random.choices(s, k=2)
            offspring = parent1.fornicate(parent2)
            new_population.append(offspring)
    
    print("Population size:", len(new_population))

    [print(f"{k}: ({max(v).fitness},{len(v)})", end=", ") for k, v in sorted(species.items())]
    print()
    EPOCH_INNOVATIONS = []

    return new_population