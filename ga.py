from math import sqrt
from random import choice, randint, sample, uniform
from sys import stdout
from time import time

# POP_LIMIT / TOURNAMENT_LIMIT must be an integer!
GENS = 5000
POP_LIMIT = 200
TOURNAMENT_LIMIT = 4
BOUNDS = 5000.0
INITIAL_MUTATION_CHANCE = 10
INITIAL_MUTATION_FACTOR = 0.05
SECONDARY_MUTATION_CHANCE = 5
SECONDARY_MUTATION_FACTOR = 0.5
CRAZY_MUTATION_CHANCE = 1

#  Create report file
timestamp = time()
f = open(str(timestamp) + '.csv','w')
f.write('Experimental\n')
f.write('POP_LIMIT: ' + str(POP_LIMIT) + '\n')
f.write('TOURNAMENT_LIMIT: ' + str(TOURNAMENT_LIMIT) + '\n')
f.write('BOUNDS: ' + str(BOUNDS) + '\n')
f.write('INITIAL_MUTATION_FACTOR: ' + str(INITIAL_MUTATION_FACTOR) + '\n')
f.write('SECONDARY_MUTATION_CHANCE: ' + str(SECONDARY_MUTATION_CHANCE) + '\n')
f.write('SECONDARY_MUTATION_FACTOR: ' + str(SECONDARY_MUTATION_FACTOR) + '\n')
f.write('CRAZY_MUTATION_CHANCE: ' + str(CRAZY_MUTATION_CHANCE) + '\n\n')
f.write('Generation, Best Fitness, Worst Fitness, Average Fitness, Best Chromosomes\n')
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
    for index, x in enumerate(X_DATA):
        y = 0
        for power, param in enumerate(candidate['chromosomes']):
            y += param*(x**power)
        y_values.append(y)
    return y_values

# Returns the fitness for a given candidate, higher is better.
# Compares calculated f(x) values to the actual ones.
def calculate_fitness(candidate):
    fitness = 0
    cand_y_values = calculate_y_values(candidate)
    for index, val in enumerate(cand_y_values):
        point_fitness = sqrt((Y_DATA[index] - val)**2)
        fitness += point_fitness
    fitness = 1 / fitness
    return fitness

# Returns a single candidate.
def generate_candidate():
    candidate = {'chromosomes': [], 'fitness': 0}
    for i in range(6):
        candidate['chromosomes'].append(uniform(-BOUNDS, BOUNDS))
    candidate['fitness'] = calculate_fitness(candidate)
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

# Randomly matches up a tournament and selects the winner. Returns a halved population.
def tournament_selection(population):
    new_population = []
    round_1 = population
    round_2 = []
    # Round 1 selects only the fittest.
    while(len(round_1) > 0):
        tournament = sample(round_1, TOURNAMENT_LIMIT)
        winner = {'fitness': 0}
        for combatant in tournament:
            if combatant['fitness'] > winner['fitness']:
                winner = combatant
            round_2.append(combatant)
            round_1.remove(combatant)
        new_population.append(winner)
    # Round 2 fills remaining slots with winners from randomly selected bouts
    while(len(new_population) < POP_LIMIT/2):
        tournament = sample(round_2, TOURNAMENT_LIMIT)
        winner = {'fitness': 0}
        for combatant in tournament:
            if combatant['fitness'] > winner['fitness']:
                winner = combatant
        new_population.append(winner)
    return new_population

# Combines the chromosomes of two parents. Returns a new population with parents and offspring.
# Doubles the current population.
def crossover(population):
    next_gen = []
    for i in range(len(population)/2):
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
        next_gen = next_gen + [create_candidate(child_1_chromosomes), create_candidate(child_2_chromosomes)]
    return next_gen

# Randomely return 1 or -1. Used to determine whether mutation increases or decreases values.
def shrink_or_grow():
    if randint(0,1) == 0:
        return -1
    return 1

# Mutates at least one chromosome in each candidate. Returns a population of original and
# mutated candidates. Doubles the size of the given population.
def mutation(population):
    mutants = []
    for candidate in population:
        if randint(1, 100) <= INITIAL_MUTATION_CHANCE:
            rand_index = randint(0,5)
            mutate_amount = shrink_or_grow() * INITIAL_MUTATION_FACTOR * candidate['chromosomes'][rand_index]
            candidate['chromosomes'][rand_index] = candidate['chromosomes'][rand_index] + mutate_amount
        if randint(1, 100) <= SECONDARY_MUTATION_CHANCE:
            rand_index = randint(0,5)
            mutate_amount = shrink_or_grow() * SECONDARY_MUTATION_FACTOR * candidate['chromosomes'][rand_index]
            candidate['chromosomes'][rand_index] = candidate['chromosomes'][rand_index] + mutate_amount
        if randint(1, 100) <= CRAZY_MUTATION_CHANCE:
            rand_index = randint(0,5)
            candidate['chromosomes'][rand_index] = uniform(-BOUNDS, BOUNDS)
        mutants.append(candidate)
    return mutants

# Performs crossover to produce offspring and applies mutation to those offspring,
# Returns a new population double the size of the old one.
def breed(population):
    new_population = population + mutation(crossover(population))
    return new_population


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
for i in range(GENS):
    population = tournament_selection(population)
    population = breed(population)
    reporter(population, i)

# custom_gen = [-0.00318,5000,5,-62,1,-0.001]
# print(custom_gen, calculate_fitness(custom_gen))
