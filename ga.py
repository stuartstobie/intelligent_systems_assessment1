from math import sqrt
from random import choice, randint, sample, uniform
from sys import stdout
from time import time

# POP_LIMIT / TOURNAMENT_LIMIT must be an even number for crossover!
GENS = 100000000
POP_LIMIT = 100
TOURNAMENT_LIMIT = 4
BOUNDS = [0.2, 10000, 1000, 100, 10, 1]
MUTATION_RATE = 0.05
UNIFORM_MUTATION_RATE = 0.005
ROUND_MUTATION_RATE = 0.005
ELITISM = True

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

# Compares calculated f(x) values to the actual ones.
# Implements the Horner Method for evaluating a polynomial.
# Returns the fitness for a given candidate, 1 is best.
def calculate_fitness(chromosomes):
    y_values = []
    for x in X_DATA:
        y = 0
        for coefficient in chromosomes[::-1]:
            y = y * x + coefficient
        y_values.append(y)
    fit = 0
    for index, val in enumerate(y_values):
        error = sqrt((Y_DATA[index] - val)**2)
        fit += error
    return 1 / (fit + 1)

# Returns a single candidate.
def generate_candidate():
    chromosomes = []
    for i in range(6):
        chromosomes.append(uniform(-BOUNDS[i], BOUNDS[i]))
    candidate = create_candidate(chromosomes)
    return candidate

# Returns a single candidate, created from given chromosomes.
def create_candidate(chromosomes):
    candidate = {'chromosomes': chromosomes, 'fitness': 0}
    candidate['fitness'] = calculate_fitness(candidate['chromosomes'])
    return candidate

# Returns an entire population, used at the start.
def generate_population():
    population = []
    for i in range(POP_LIMIT):
        population.append(generate_candidate())
    return population

def get_fittest(population):
    fittest = {'fitness': 0}
    for candidate in population:
        if candidate['fitness'] > fittest['fitness']:
            fittest = candidate
    return fittest

# Randomly matches up a tournament and selects the winner. Returns a reduced population (0.25).
def tournament_selection(population):
    tournament = sample(population, TOURNAMENT_LIMIT)
    return get_fittest(tournament)

# Combines the chromosomes of two parents in one of two ways. Returns a new population of offspring.
def crossover(parent_1, parent_2):
    offspring_chromosomes = []
    for i in range(0,6):
        if randint(0,1) == 0:
            offspring_chromosomes.append(parent_1['chromosomes'][i])
        else:
            offspring_chromosomes.append(parent_2['chromosomes'][i])
    return offspring_chromosomes

# Mutates at least one chromosome in each candidate. Returns a population of mutated candidates.
def mutate(chromosomes):
    for i in range(len(chromosomes)):
        if uniform(0,1) < UNIFORM_MUTATION_RATE:
            chromosomes[i] = uniform(-BOUNDS[i], BOUNDS[i])
        if uniform(0,1) < MUTATION_RATE:
            mutation_factor = uniform(-0.1, 0.1)
            chromosomes[i] = chromosomes[i] + mutation_factor * chromosomes[i]
        if uniform(0,1) < ROUND_MUTATION_RATE:
            chromosomes[i] = round(chromosomes[i], randint(1,5))
    return chromosomes

def evolve_population(population):
    new_population = []
    # Keep the best candidate from previous generation if ELITISM == True
    elitism_offset = 0
    if ELITISM:
        new_population.append(get_fittest(population))
        elitism_offset = 1
    # Crossover population
    for i in range(elitism_offset, POP_LIMIT):
        parent_1 = tournament_selection(population)
        parent_2 = tournament_selection(population)
        # and mutate the offspring
        offspring_chromosomes = mutate(crossover(parent_1, parent_2))
        new_population.append(create_candidate(offspring_chromosomes))
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
    stdout.write("Generation: %d, Best: %-10.20f \r" % (i, best['fitness']))
    stdout.flush()

# population = generate_population()
# print('BEFORE ', population)
# population = evolve_population(population)
# print('AFTER ',population)

# Create initial population
population = generate_population()
# Loops through the selection, crossover and mutation phases for given number of genereations.
for i in range(GENS+1):#
    population = evolve_population(population)
    if i == 50000:
        TOURNAMENT_LIMIT = 5
        ROUND_MUTATION_RATE = 0.01
    if i == 100000:
        TOURNAMENT_LIMIT = 6
        ROUND_MUTATION_RATE = 0.02
    if i == 500000:
        TOURNAMENT_LIMIT = 8
        UNIFORM_MUTATION_RATE = 0.01
        ROUND_MUTATION_RATE = 0.03
    if i == 1000000:
        TOURNAMENT_LIMIT = 10
        MUTATION_RATE = 0.8
        UNIFORM_MUTATION_RATE = 0.02
        ROUND_MUTATION_RATE = 0.05
    if i%100 == 0:
        reporter(population, i)

# custom_gen = {'chromosomes':[-0.00318, 5000, 5, -62, -0.001]}
# print(calculate_fitness(custom_gen))
