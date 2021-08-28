from __future__ import print_function

import copy
import warnings

import graphviz
import matplotlib.pyplot as plt
import numpy as np


def plot_stats(statistics, ylog=False, view=False, filename='avg_fitness.svg'):
    """ Plots the population's average and best fitness. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = np.array(statistics.get_fitness_mean())
    stdev_fitness = np.array(statistics.get_fitness_stdev())

    plt.plot(generation, avg_fitness, 'b-', label="average")
    #plt.plot(generation, avg_fitness - stdev_fitness, 'g-.', label="-1 sd")
    plt.plot(generation, avg_fitness + stdev_fitness, 'g-.', label="+1 sd")
    plt.plot(generation, best_fitness, 'r-', label="best")

    plt.title("Population's average and best fitness")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")
    plt.grid()
    plt.legend(loc="best")
    if ylog:
        plt.gca().set_yscale('symlog')

    plt.savefig(filename)
    if view:
        plt.show()

    plt.close()


def plot_spikes(spikes, view=False, filename=None, title=None):
    """ Plots the trains for a single spiking neuron. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    t_values = [t for t, I, v, u in spikes]
    v_values = [v for t, I, v, u in spikes]
    u_values = [u for t, I, v, u in spikes]
    I_values = [I for t, I, v, u in spikes]

    fig = plt.figure()
    plt.subplot(3, 1, 1)
    plt.ylabel("Potential (mv)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, v_values, "g-")

    if title is None:
        plt.title("Izhikevich's spiking neuron model")
    else:
        plt.title("Izhikevich's spiking neuron model ({0!s})".format(title))

    plt.subplot(3, 1, 2)
    plt.ylabel("Recovery (u)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, u_values, "r-")

    plt.subplot(3, 1, 3)
    plt.ylabel("Current (I)")
    plt.xlabel("Time (in ms)")
    plt.grid()
    plt.plot(t_values, I_values, "r-o")

    if filename is not None:
        plt.savefig(filename)

    if view:
        plt.show()
        plt.close()
        fig = None

    return fig


def plot_species(statistics, view=False, filename='speciation.svg'):
    """ Visualizes speciation throughout evolution. """
    if plt is None:
        warnings.warn("This display is not available due to a missing optional dependency (matplotlib)")
        return

    species_sizes = statistics.get_species_sizes()
    num_generations = len(species_sizes)
    curves = np.array(species_sizes).T

    fig, ax = plt.subplots()
    ax.stackplot(range(num_generations), *curves)

    plt.title("Speciation")
    plt.ylabel("Size per Species")
    plt.xlabel("Generations")

    plt.savefig(filename)

    if view:
        plt.show()

    plt.close()


def draw_net(config, genome, view=False, filename=None, node_names=None, show_disabled=True, prune_unused=False,
             node_colors=None, n_labels=None, fmt='svg'):
    """ Receives a genome and draws a neural network with arbitrary topology. """
    # Attributes for network nodes.
    if graphviz is None:
        warnings.warn("This display is not available due to a missing optional dependency (graphviz)")
        return

    if node_names is None:
        node_names = {}

    assert type(node_names) is dict

    if node_colors is None:
        node_colors = {}

    assert type(node_colors) is dict

    node_attrs = {
        'shape': 'circle',
        'fontpath':'C:\Windows\Fonts',
        'fontname':'Sans',
        'fontsize': '20',
        'height': '0.2',
        'width': '0.2'}
    graph_attrs = {
        'rankdir' : 'LR',
        'nodesep':'.1',
        'ranksep':'1',
        'spline':'true',
        'dpi':'300'
        }

    dot = graphviz.Digraph(format=fmt, node_attr=node_attrs, graph_attr = graph_attrs)
    
    with dot.subgraph(name='input_level') as c:
        inputs = set()
        for k in config.genome_config.input_keys:
            inputs.add(k)
            name = node_names.get(k, str(k))
            _label = n_labels.get(k, str(-k))
            input_attrs = {'style': 'filled',
                           'shape': 'circle',
                           'fixedsize':'true',
                           'height':'.3',
                           'rank':str(-k)
                           }
            input_attrs['fillcolor'] = node_colors.get(k, 'lightblue')
            c.graph_attr = {'rank':'same','ordering':'out'}
            c.node(name, label=_label, _attributes=input_attrs)


    with dot.subgraph(name='output_level') as c:
        outputs = set()
        for k in config.genome_config.output_keys:
            outputs.add(k)
            name = node_names.get(k, str(k))
            _label = n_labels.get(k, str(k))
            node_attrs = {'style': 'filled', 'fontsize':'30'}
            node_attrs['fillcolor'] = node_colors.get(k, 'orange')
            c.graph_attr = {'rank':'same'}
            c.node(name,  label=_label,_attributes=node_attrs)


    if prune_unused:
        connections = set()
        for cg in genome.connections.values():
            if cg.enabled or show_disabled:
                connections.add(cg.key)

        used_nodes = copy.copy(outputs)
        pending = copy.copy(outputs)
        while pending:
            new_pending = set()
            for a, b in connections:
                if b in pending and a not in used_nodes:
                    new_pending.add(a)
                    used_nodes.add(a)
            pending = new_pending
    else:
        used_nodes = set(genome.nodes.keys())

    with dot.subgraph(name='mid_level') as c:
        for n in used_nodes:
            if n in inputs or n in outputs:
                continue
    
            attrs = {'style': 'filled','fixedsize':'true',
                           'height':'.3','fontsize':'9'}
            attrs['fillcolor'] = node_colors.get(n, 'lightgray')
            c.graph_attr = {'rank':'same'}
            c.node(str(n), _attributes=attrs)


    for i in range(len(config.genome_config.input_keys)-1):
        k1 = config.genome_config.input_keys[i]
        k2 = config.genome_config.input_keys[i+1]
        a = node_names.get(k1, str(k1))
        b = node_names.get(k2, str(k2))
        dot.edge(a, b, _attributes={'style': 'invis'})
        
    for cg in genome.connections.values():
        if cg.enabled or show_disabled:
            #if cg.input not in used_nodes or cg.output not in used_nodes:
            #    continue
            input, output = cg.key
            a = node_names.get(input, str(input))
            b = node_names.get(output, str(output))
            style = 'solid' if cg.enabled else 'dotted'
            color = 'green' if cg.weight > 0 else 'red'
            width = str(0.1 + abs(cg.weight / 5.0)+.6)
            dot.edge(a, b, _attributes={'style': style, 'color': color, 'penwidth': width})

    dot.render(filename, view=view, format='png')

    return dot
