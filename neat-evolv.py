
import multiprocessing
import os
import pickle
import numpy as np
import neat
import time
import threading
from Game_GUI import GameGUI
import os
os.environ['path'] += r';C:\Users\Akhil\AppData\Local\Programs\GIMP 2\bin'
import cairosvg

from SnakeGame import SnakeGame

import visualize


runs_per_net = 3
finished = False

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    
    fitnesses = []

    for runs in range(runs_per_net):
        sim = SnakeGame(10)

        # Run the given simulation for up to num_steps time steps.
        fitness = 0.0
        done = False
        inputs = sim.get_observation()
        while not done:
            action = [0,0]
            max_index = np.argmax(net.activate(inputs))
            if max_index<2:
                action[max_index]=1
            #print(f'The selected action {action}')
            inputs, reward, done = sim.step(action)
            fitness += reward
        
        fitness = sim.steps + (2**fitness + (fitness**2.1)*500) - (fitness**1.2*((0.25**sim.steps)**1.3))
        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
    return np.max(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))
    

    x = threading.Thread(target=visualise_genomes, args=(pop,config,))
    x.start()
    
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)
    finished = True

    # visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    # visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    # node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    # visualize.draw_net(config, winner, True, node_names=node_names)

    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                     filename="winner-feedforward.gv")
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                     filename="winner-feedforward-enabled.gv", show_disabled=False)
    # visualize.draw_net(config, winner, view=True, node_names=node_names,
    #                     filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)

def visualise_network(winner, config):
    #visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    #visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                        filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                        filename="winner-feedforward-enabled.gv", show_disabled=False)
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                        filename="winner-feedforward-enabled-pruned.gv", show_disabled=False, prune_unused=True)

def save_genome_date(gen, genome, config):
    
    with open(f'gen\genome {gen}', 'wb') as f:
        pickle.dump(genome, f)
    
    arrows = ['↑', '<&#x2196;>', '←', '<&#x2199;>', '↓', '<&#x2198;>', '→', '<&#x2197;>']
    arrows = arrows + arrows + ['∡']
    output_labels = ['<&#8624;>','<&#8625;>','↑']
    node_labels = {}
    for i in range(1,18):
        node_labels[-i]= arrows[i-1]
    for i in range(0,3):
        node_labels[i]= output_labels[i]

    node_colors = {}
    for i in range (1,9):
        node_colors[-i]='olivedrab1'
    for i in range (9,17):
        node_colors[-i]='pink2'
    node_colors[-17]='lightblue'
    for i in range (0,4):
        node_colors[i]='khaki'
    
    visualize.draw_net(config, genome, filename=f'gen\genome_struct {gen}',
                       n_labels=node_labels, show_disabled=False, prune_unused=False,
                       node_colors=node_colors, fmt='png')
    return f'gen\genome_struct {gen}.png'
  
def visualise_genomes(pop, config):
    i=500
    lazytime = 500
    last_genome = None
    all_time_best = 0
  
    while i>0:
        if last_genome != None and last_genome == pop.best_genome:
            time.sleep(2)
            lazytime -=1
            if lazytime<0:
                break
        else:
            lazytime=500

        best_genom = pop.best_genome
        if best_genom!= None:
            #visualise_network(best_genom, config)
            net = neat.nn.FeedForwardNetwork.create(best_genom, config)
            gen_no = pop.generation
            sim = SnakeGame(10)
            inputs = sim.get_observation()
            done = False
            gui = GameGUI(10,sim)
            gui.txt_high_score = all_time_best
            try:
                png_file_name = save_genome_date(gen_no, best_genom, config)
                gui.load_genome_struct_img(png_file_name)
            except:
                print('UNINTENTIONAL EROOR OCCURED')
                
            while not done:
                gui.txt_gen = gen_no
                gui.txt_score = sim.snake.size-3
                if gui.txt_high_score < gui.txt_score:
                    gui.txt_high_score = gui.txt_score
                    all_time_best = gui.txt_score
                action = [0,0]
                max_index = np.argmax(net.activate(inputs))
                if max_index<2:
                    action[max_index]=1
                inputs, _, done = sim.step(action)
                res = gui.draw()
                if res==False:
                    break
                time.sleep(0.2)
            last_genome = best_genom
            i=500
            gui.close()
        else:
            time.sleep(2)
            i -=1

if __name__ == '__main__':
    run()