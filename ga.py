from math import sqrt
from random import choice, randint, sample, uniform
from sys import stdout
from time import time

# POP_LIMIT / TOURNAMENT_LIMIT must be an even number for crossover!
GENS = 100000
POP_LIMIT = 240
TOURNAMENT_LIMIT = 4 # MUST be 4 or higher
BOUNDS = 5000.0
UNIFORM_MUTATION_CHANCE = 5
BOUNDARY_MUTATION_CHANCE = 2

#  Create report file
timestamp = time()
f = open(str(timestamp) + '.csv','w')
f.write('POP_LIMIT: ' + str(POP_LIMIT) + '\n')
f.write('TOURNAMENT_LIMIT: ' + str(TOURNAMENT_LIMIT) + '\n')
f.write('BOUNDS: ' + str(BOUNDS) + '\n')
f.write('Generation, Best, Worst, Average, Best Chromosomes\n')
f.close()

# Open data file
data_file = open('datfile.dat', 'r')
# create float array from data_file, splitting on whitespace
data = [float(x) for x in data_file.read().split()]
# close data_file
data_file.close()
# create two arrays for x and y data
X_DATA = data[::2] # even values are x coordinates
Y_DATA = data[1::2] # odd values are y coordinates

# Returns f(x) values for a given candidate. Used in fitness calculation.
def calculate_y_values(candidate):
    y_values = []
    for x in X_DATA:
        y = horner(x, candidate['chromosomes'])
        y_values.append(y)
    return y_values

# A function that implements the Horner Scheme for evaluating a
# polynomial of coefficients polynomial in x. Uses reversed array.
def horner(x, polynomial):
    result = 0
    for coefficient in polynomial:
        result = result * x + coefficient
    return result

# Returns the fitness for a given candidate, higher is better.
# Compares calculated f(x) values to the actual ones.
def calculate_fitness(candidate):
    fitness = 0
    cand_y_values = calculate_y_values(candidate)
    for index, val in enumerate(cand_y_values):
        error = sqrt((Y_DATA[index] - val)**2)
        fitness += error
    fitness = 1 / (fitness + 1)
    return fitness

# Returns a single candidate.
def generate_candidate():
    chromosomes = []
    for i in range(6):
        chromosomes.append(uniform(-BOUNDS, BOUNDS))
    candidate = create_candidate(chromosomes)
    return candidate

# Returns a single candidate, created from given chromosomes.
def create_candidate(chromosomes):
    candidate = {'chromosomes': chromosomes, 'fitness': 0}
    candidate['fitness'] = calculate_fitness(candidate)
    return candidate

# Returns an entire population, used at the start.
def generate_population():
    population = []
    for i in range(POP_LIMIT):
        population.append(generate_candidate())
    return population

# Randomly matches up a tournament and selects the winner. Returns a reduced population (0.25).
def tournament_selection(population):
    new_population = []
    round_1 = population
    round_2 = []
    # Round 1 selects only the fittest. All combatants compete at least once.
    while(len(round_1) > 0):
        tournament = sample(round_1, TOURNAMENT_LIMIT)
        winner = {'fitness': 0}
        for combatant in tournament:
            if combatant['fitness'] > winner['fitness']:
                winner = combatant
            round_2.append(combatant)
            round_1.remove(combatant)
        new_population.append(winner)
    # Round 2 fills remaining slots with winners from randomly selected bouts (only used if TOURNAMENT_LIMIT > 4)
    while(len(new_population) < POP_LIMIT/4):
        tournament = sample(round_2, TOURNAMENT_LIMIT)
        winner = {'fitness': 0}
        for combatant in tournament:
            if combatant['fitness'] > winner['fitness']:
                winner = combatant
        new_population.append(winner)
    return new_population

# Combines the chromosomes of two parents in one of two ways. Returns a new population of offspring.
def crossover(population):
    offspring = []
    for i in range(int(len(population)/2)):
        parent_1 = population[2*i]
        parent_2 = population[2*i+1]
        child_1_chromosomes = []
        child_2_chromosomes = []
        if randint(0,1) == 0:
            child_1_chromosomes = parent_1['chromosomes'][:3] + parent_2['chromosomes'][-3:]
            child_2_chromosomes = parent_2['chromosomes'][:3] + parent_1['chromosomes'][-3:]
        else:
            child_1_chromosomes = [parent_1['chromosomes'][0], parent_2['chromosomes'][1],parent_1['chromosomes'][2], parent_2['chromosomes'][3], parent_1['chromosomes'][4], parent_2['chromosomes'][5]]
            child_2_chromosomes = [parent_2['chromosomes'][0], parent_1['chromosomes'][1], parent_2['chromosomes'][2], parent_1['chromosomes'][3], parent_2['chromosomes'][4], parent_1['chromosomes'][5]]
        offspring = offspring + [create_candidate(child_1_chromosomes), create_candidate(child_2_chromosomes)]
    return offspring

# Randomely return 1 or -1. Used to determine whether mutation increases or decreases values.
def shrink_or_grow():
    if randint(0,1) == 0:
        return -1
    return 1

# Mutates at least one chromosome in each candidate. Returns a population of mutated candidates.
def mutation(population):
    mutants = []
    for candidate in population:
        mutant_chromosomes = candidate['chromosomes']
        # Non-Uniform Mutation
        rand_index = randint(0,5)
        mutation_factor = uniform(0.05, 0.5)
        mutation_amount = mutation_factor * mutant_chromosomes[rand_index]
        mutant_chromosomes[rand_index] = mutant_chromosomes[rand_index] + shrink_or_grow() * mutation_amount
        # Uniform Mutation
        if randint(0,100) < UNIFORM_MUTATION_CHANCE:
            rand_index = randint(0,5)
            mutant_chromosomes[rand_index] = mutant_chromosomes[rand_index] + uniform(-BOUNDS/4, BOUNDS/4)
        if randint(0,100) < BOUNDARY_MUTATION_CHANCE:
            rand_index = randint(0,5)
            mutant_chromosomes[rand_index] = shrink_or_grow() * BOUNDS
        mutants.append(create_candidate(mutant_chromosomes))
    return mutants

# Writes to the report file for the given population updates the stdout.
def reporter(population, gen):
    best = population[1]
    worst = best
    total_fitness = 0
    for candidate in population:
        if candidate['fitness'] > best['fitness']:
            best = candidate
        if candidate['fitness'] < worst['fitness']:
            worst = candidate
        total_fitness += candidate['fitness']
    average = total_fitness / len(population)
    f = open(str(timestamp) + '.csv','a')
    f.write(str(i) + ', ')
    f.write(str(best['fitness']) + ', ')
    f.write(str(worst['fitness']) + ', ')
    f.write(str(average) + ', ')
    f.write(str(best['chromosomes']) + '\n')
    f.close()
    stdout.write("Generation: %d, Best: %-10.20f \r" % (i, best['fitness']) )
    stdout.flush()

# Create initial population
population = generate_population()
# Loops through the selection, crossover and mutation phases for given number of genereations.
for i in range(GENS+1):#
    if i == 3000:
        TOURNAMENT_LIMIT = 5
    if i == 6000:
        TOURNAMENT_LIMIT = 6
    if i == 10000:
        TOURNAMENT_LIMIT = 10
    population = tournament_selection(population)
    population = population + crossover(population)
    population = population + mutation(population)
    if i%100 == 0:
        reporter(population, i)

# custom_gen = {'chromosomes':[-0.001, 1, -62, 5, 5000, -0.00318]}
# print(calculate_fitness(custom_gen))
