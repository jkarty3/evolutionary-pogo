# This file allows a user to control the pogo stick. Use a and d to extend and retract the bottom left spring. Use → and ← to extend and retract
# the top right spring. Use space bar to jump.
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

# Initialize the pymunk physics engine
pogo = Pogo()
pygame.init()
screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Keep track of agents and population
tic = time.time()
toc = time.time()

# Simulation loop
running = True
player_response = [0, 0, 0, 0, 0]
while running:
    # get current state and players response
    current_state = pogo.get_current_state()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:# exit out of the game if x is pressed
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_response[0] = 1
            elif event.key == pygame.K_RIGHT:
                player_response[1] = 1
            elif event.key == pygame.K_LEFT:
                player_response[2] = 1
            elif event.key == pygame.K_d:
                player_response[3] = 1
            elif event.key == pygame.K_a:
                player_response[4] = 1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                player_response[0] = 0
            elif event.key == pygame.K_RIGHT:
                player_response[1] = 0
            elif event.key == pygame.K_LEFT:
                player_response[2] = 0
            elif event.key == pygame.K_d:
                player_response[3] = 0
            elif event.key == pygame.K_a:
                player_response[4] = 0
    
    # apply those actions to the simulation
    pogo.apply_actions(player_response)


    if abs(current_state[0])<1.4: # if it falls over, wait a little bit to let it slide
        toc = time.time()

    if time.time()-tic > 10 or time.time()-toc > 0.5: # fell over or ran out of time
        print(f"You reached position {current_state[2] - 300}")

        #reset simulation
        tic = time.time()
        pogo.reset_simulation()

    
    # Step the simulation forward
    pogo.space.step(1 / 60.0)

    # Draw the objects
    screen.fill((255, 255, 255))
    pogo.space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()