from SnakeGame import SnakeGame
from Game_GUI import GameGUI
import time
import random
import neat
import visualize
import os
import pickle


# sg = SnakeGame(10)
# gui = GameGUI(10,sg)

# local_dir = os.path.dirname(__file__)
# config_path = os.path.join(local_dir, 'config-feedforward')
# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_path)

# with open('gen\genome 67', 'rb') as f:
#     c = pickle.load(f)
 
# arrows = ['↑', '<&#x2196;>', '←', '<&#x2199;>', '↓', '<&#x2198;>', '→', '<&#x2197;>']
# arrows = arrows + arrows + ['∡']
# output_labels = ['<&#8624;>','<&#8625;>','↑']
# node_labels = {}
# for i in range(1,18):
#     node_labels[-i]= arrows[i-1]
# for i in range(0,3):
#     node_labels[i]= output_labels[i]


# node_colors = {}
# for i in range (1,9):
#     node_colors[-i]='olivedrab1'
# for i in range (9,17):
#     node_colors[-i]='pink2'
# node_colors[-17]='lightblue'
# for i in range (0,4):
#     node_colors[i]='khaki'
# visualize.draw_net(config, c, view=True, filename='tk', 
#                     n_labels=node_labels, show_disabled=False, 
#                     prune_unused=False,
#                     node_colors=node_colors, fmt='png')    

sg = SnakeGame(10)
gui = GameGUI(10,sg)
gui.load_genome_struct_img('gen\genome_struct 2.png')
done = False
while not done:
    #print(sg)
    gui.draw()
    time.sleep(2)
    action = [0,0,0]
    rand_id = random.randint(0, 2)
    action[rand_id] = 1
    _, _, done = sg.step(action[0:2])
gui.close()

# import pickle
# with open('winner-feedforward', 'rb') as f:
#     c = pickle.load(f)
    
# local_dir = os.path.dirname(__file__)
# config_path = os.path.join(local_dir, 'config-feedforward')
# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                          neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                          config_path)
# visualize.draw_net(config, c, view=True, filename='test121212', 
#                    node_names=None, show_disabled=True, 
#                    prune_unused=True,
#                    node_colors=None, fmt='svg')


# import pygame


# WIDTH = 800
# HEIGHT = 600
# pygame.init()
# window = pygame.display.set_mode((WIDTH, HEIGHT))
# screen = pygame.display.get_surface()

# pygame.display.flip() 

# import os
# os.environ['path'] += r';C:\Users\Akhil\AppData\Local\Programs\GIMP 2\bin'
# import cairosvg
# cairosvg.svg2png(url='test121212.svg', write_to='img.png')

# img = pygame.image.load('img.png')
# img = pygame.transform.rotate(img, 90)
# img = pygame.transform.scale(img, (200,600))
# clock = pygame.time.Clock()
# while True:
#     screen.blit(img,(0,0))
#     pygame.display.update()
#     clock.tick(15)
#     event = pygame.event.get()
#     for e in event:
#         if e.type == 12:
#             raise SystemExit

