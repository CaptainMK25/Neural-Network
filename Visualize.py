from manim import *
import numpy as np
from utils import visual


def receive_inputs():
    global inputs, hlayers, outputs
    variables = visual.receive_neural_network()
    inputs = variables[0]
    hlayers = variables[1]
    outputs = variables[2]


class VisualizeNeuralNetwork(Scene):

    def construct(self):
        layers = hlayers
        layers.insert(0, inputs)
        layers.append(outputs)

        middle_layer_index = (len(layers) - 1) / 2

        highest_num__layer_nodes = visual.get_highest_number_of_nodes(layers)

        variables = visual.optimize_variables(len(layers), highest_num__layer_nodes)

        length_between_layers = variables[0]
        length_between_nodes = variables[1]
        node_radius = variables[2]

        for i in range(len(layers)):
            current_layer = layers[i]
            current_layer_index = i
            middle_node_index = (len(current_layer) - 1) / 2

            for j in range(len(current_layer)):
                current_node = current_layer[j]
                current_node_index = j
                x_coordinate = visual.get_coordinate(middle_layer_index, current_layer_index, length_between_layers, node_radius)
                y_coordinate = visual.get_coordinate(middle_node_index, current_node_index, length_between_nodes, node_radius)

                node = Circle(node_radius)

                node.move_to((x_coordinate, y_coordinate, 0))
                self.add(node)


    def play(self):
        self.render()




'''
At this point, we have a way to get the following variables:
- Layers list
- Current number of nodes in the layer
- Length between layers
- Length between nnodes
- Node radius

Here's the plan:
We will have 2 for loops, one loop going through the layers, the other going through the nodes of the layer
Outside all loops, we want to get the middle_layer_index. We will get the length between layers, length between nodes and node radius, by running the optimization function with the highest number of nodes in a layer
Inside the layers loop, we want to get the current_layer_index, middle_node_index
Inside the nodes loop, we want to get the coordinates for each node, create and play it on the frame
'''