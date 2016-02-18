# TODO May only need sqrt from math and uniform from random
import math
import random

POP_LIMIT = 80
TOURNAMENT_LIMIT = 4
BOUND = 10000.0

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
        for power, param in enumerate(candidate):
            y += param*(x**power)
        y_values.append(y)
    return y_values

def calculate_fitness(candidate):
    fitness = 0
    cand_y_values = calculate_y_values(candidate)
    for index, val in enumerate(cand_y_values):
        point_fitness = math.sqrt((Y_DATA[index] - val)**2)
        fitness += point_fitness
    return fitness

def generate_candidate():
    candidate = []
    for i in range(6):
        candidate.append(random.uniform(BOUND, -BOUND))
    return candidate

def generate_population():
    population = []
    for i in range(POP_LIMIT):
        population.append(generate_candidate())
    return population

# def tournament_selection(population):
#     new_population = []
#     while(len(population) > 0):
#         tornament = population[:TOURNAMENT_LIMIT:]
#         for combatant in tournament:
#
#         del population[:TOURNAMENT_LIMIT:]

custom_gen = [-0.00318,5000,5,-62,1,-0.001]
print(calculate_fitness(custom_gen))
