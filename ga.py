# TODO May only need sqrt from math and uniform from random
from math import sqrt
from random import choice, randint, sample, uniform

# POP_LIMIT / TOURNAMENT_LIMIT must be an even number for crossover!
POP_LIMIT = 200
TOURNAMENT_LIMIT = 4
BOUNDS = 1000.0
INITIAL_MUTATION_FACTOR = 0.1
SECONDARY_MUTATION_CHANCE = 10
SECONDARY_MUTATION_FACTOR = 0.8
CRAZY_MUTATION_CHANCE = 5

# Open data file
data_file = open('datfile.dat', 'r')
# create float array from data_file, splitting on whitespace
data = [float(x) for x in data_file.read().split()]
# close data_file
data_file.close()
# create two arrays for x and y data
X_DATA = data[::2] # even values are x coordinates
Y_DATA = data[1::2] # odd values are y coordinates

def calculate_y_values(candidate):
    y_values = []
    for index, x in enumerate(X_DATA):
        y = 0
        for power, param in enumerate(candidate['chromosomes']):
            y += param*(x**power)
        y_values.append(y)
    return y_values

def calculate_fitness(candidate):
    fitness = 0
    cand_y_values = calculate_y_values(candidate)
    for index, val in enumerate(cand_y_values):
        point_fitness = sqrt((Y_DATA[index] - val)**2)
        fitness += point_fitness
    fitness = 1 / fitness
    return fitness

def generate_candidate():
    candidate = {'chromosomes': [], 'fitness': 0}
    for i in range(6):
        candidate['chromosomes'].append(uniform(-BOUNDS, BOUNDS))
    candidate['fitness'] = calculate_fitness(candidate)
    return candidate

def create_candidate(chromosomes):
    candidate = {'chromosomes': chromosomes, 'fitness': 0}
    candidate['fitness'] = calculate_fitness(candidate)
    return candidate

def generate_population():
    population = []
    for i in range(POP_LIMIT):
        population.append(generate_candidate())
    return population

def tournament_selection(population):
    new_population = []
    while(len(population) > 0):
        tournament = sample(population, TOURNAMENT_LIMIT)
        winner = {'fitness': 0}
        for combatant in tournament:
            if combatant['fitness'] > winner['fitness']:
                winner = combatant
            population.remove(combatant)
        new_population.append(winner)
    return new_population

def crossover(population):
    new_population = []
    next_gen = []
    while(len(population) > 0):
        parent_1 = population.pop(population.index(choice(population)))
        parent_2 = population.pop(population.index(choice(population)))
        child_1_chromosomes = parent_1['chromosomes'][:3] + parent_2['chromosomes'][-3:]
        child_2_chromosomes = parent_1['chromosomes'][-3:] + parent_2['chromosomes'][:3]
        next_gen = next_gen + [create_candidate(child_1_chromosomes), create_candidate(child_2_chromosomes)]
        new_population = new_population + [parent_1, parent_2]
    new_population = new_population + next_gen
    return new_population

def shrink_or_grow():
    if randint(0,1) == 0:
        return -1
    return 1

def mutation(population):
    mutants = []
    for candidate in population:
        mutant_chromosomes = candidate['chromosomes']
        rand_index = randint(0,5)
        mutate_amount = shrink_or_grow() * INITIAL_MUTATION_FACTOR * mutant_chromosomes[rand_index]
        mutant_chromosomes[rand_index] = mutant_chromosomes[rand_index] + mutate_amount
        if randint(1, 100) <= SECONDARY_MUTATION_CHANCE:
            rand_index = randint(0,5)
            mutate_amount = shrink_or_grow() * SECONDARY_MUTATION_FACTOR * mutant_chromosomes[rand_index]
            mutant_chromosomes[rand_index] = mutant_chromosomes[rand_index] + mutate_amount
        if randint(1, 100) <= CRAZY_MUTATION_CHANCE:
            rand_index = randint(0,5)
            mutant_chromosomes[rand_index] = uniform(-BOUNDS, BOUNDS)
        mutants.append(create_candidate(mutant_chromosomes))
    population = population + mutants
    return population

def top_up(population):
    # if len(population) < POP_LIMIT:
    #     print('Topping up: ', POP_LIMIT - len(population))
    while(len(population) < POP_LIMIT):
        population.append(generate_candidate())

def reporter(population):
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
    print('Best: ', best['fitness'])
    print(best['chromosomes'])
    print('Worst:', worst['fitness'])
    print('Average: ', average)

population = generate_population()

for i in range(0,10000):
    population = tournament_selection(population)
    population = crossover(population)
    population = mutation(population)
    top_up(population)
    print('Generation: ', i, 'Population: ', len(population))
    reporter(population)

# population = generate_population()
# print(len(population))
# population = tournament_selection(population)
# print(len(population))

# custom_gen = [-0.00318,5000,5,-62,1,-0.001]
# print(custom_gen, calculate_fitness(custom_gen))
