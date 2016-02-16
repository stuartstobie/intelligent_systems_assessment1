# TODO May only need sqrt from math and uniform from random
import math
import random


UPPER_BOUND = -100.0
LOWER_BOUND = 100.0

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

def calculate_fitness(calculated_y):
    fitness = 0
    for index, val in enumerate(calculated_y):
        point_fitness = math.sqrt((Y_DATA[index] - val)**2)
        fitness += point_fitness
    return fitness

def generate_candidate():
    candidate = []
    for i in range(6):
        candidate.append(random.uniform(UPPER_BOUND, LOWER_BOUND))
    return candidate

cand = generate_candidate()
ys = calculate_y_values(cand)
print(cand, calculate_fitness(ys))
