# This file randomly creates a population of agents and trains them. It prints out the weights and biases of the best agent from each generation
# for the user to copy and paste into the checkpoint file. It also prints the overall best agent at the end of training, as well as graphing the
# results. The goal of the agent is to move to the right.
#
# Jacob Karty 12/3/2024

from Pogo import Pogo
import pygame
import pymunk
import pymunk.pygame_util
from NeuralNet import NeuralNetwork
import time
import numpy as np
import matplotlib.pyplot as plt

# Training parameters - edit these within reason
population_size = 30
mutation_rate = 0.1
elitism = True
annealing = True # this annealing is for the mutation rate
annealing_step_size = 0.001
annealing_min = .01
hidden_layers = [20, 20, 20, 20, 20, 20]

# Initialize the pymunk physics engine
pogo = Pogo()
pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create the neural network population
population = []
evaluation = []
agent_distances = []
layers = [12]
for layer in hidden_layers:
    layers.append(layer)
layers.append(5)
for i in range(population_size):
    population.append(NeuralNetwork(layers))
    evaluation.append(0)
    agent_distances.append(0)

# Keep track of agents and population
tic = time.time()
toc = time.time()
current_agent = 0
fitness_plot = []
best_distance = 0
best_agent = 0
generation_number = 0
print("Generation 0:")

# Simulation loop
running = True
while running:
    #get current state, determine agents response, and apply those responses to the environment
    current_state = pogo.get_current_state()
    agent_response = population[current_agent].calculate_forward(current_state)
    pogo.apply_actions(agent_response)

    # Switch between agents. Give each agent 10 seconds before evaluating it, or if it falls over. Also keep track of when the
    # generation is over and make a new one
    if abs(current_state[0])<1.4: # if it falls over, wait a little bit to let it slide
        toc = time.time()

    if time.time()-tic > 10 or time.time()-toc > 0.5:
        #determine the fitness of the agent
        agent_distances[current_agent] = current_state[2] - 300
        evaluation[current_agent] = agent_distances[current_agent] + (time.time()-tic) * 10 # this is the position of the agent plus how long it stayed up, encouraging the agent to both stay up and move further
        print(f"Agent {current_agent} reached position {agent_distances[current_agent]} with fitness {evaluation[current_agent]}")
        if agent_distances[current_agent] > best_distance: #keep track of the best agent
            best_agent = population[current_agent]
            best_distance = agent_distances[current_agent]

        #reset simulation
        current_agent += 1
        tic = time.time()
        pogo.reset_simulation()

        if current_agent == population_size: # if the entire population has run
            # find the average fitness for plotting later
            avg = sum(evaluation) / len(evaluation)
            fitness_plot.append(avg)

            #sort by the best agents
            top_indices = np.argsort(evaluation)[::-1]
            print(f"The best agent reached {agent_distances[top_indices[0]]} with fitness {evaluation[top_indices[0]]}")
            population[top_indices[0]].print_network()

            #take top 20% of population and make the next generation
            children = []
            num_top_agents = population_size//5

            if elitism: #keep the top 20% of population in the next genreation
                for i in range(num_top_agents):
                    children.append(population[top_indices[i]])
            
            #determine which agents reproduce with which other agents and how many times
            reproduction_matrix = NeuralNetwork.generate_weighted_reproduction_matrix(num_top_agents, population_size - len(children))
            for i in range(len(reproduction_matrix)):
                for j, value in enumerate(reproduction_matrix[i]):
                    for k in range(value):
                        children.append(population[top_indices[i]].make_child(population[top_indices[j]], mutation_rate)) #make the child
            generation_number += 1
            print(f'Generation {generation_number}:')
            population = children
            current_agent = 0

            #annealing - cool off the mutation rate slowly
            if annealing:
                mutation_rate -= annealing_step_size
            if mutation_rate < annealing_min:
                mutation_rate = annealing_min

    # exit out of the game if x is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Step the simulation forward
    pogo.space.step(1 / 60.0)

    # Draw the objects
    screen.fill((255, 255, 255))
    pogo.space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()


#print the best agent
print(f'The overall best agent reached {best_distance}')
best_agent.print_network()

#plot the average fitness throughout
plt.plot(fitness_plot, marker='o', linestyle='-', color='b')
plt.title('Pogostick Evolution')
plt.xlabel('Generation')
plt.ylabel('Average Fitness')
plt.legend()
plt.grid(True)
plt.show()