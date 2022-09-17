from manim import *
import numpy as np
from utils.visuals import visual_helpers


class VisualizeNeuralNetwork(Scene):

    def construct(self):
        layers = hlayers
        layers.insert(0, [[i] for i in inputs])
        layers.append(outputs)

        middle_layer_index = (len(layers) - 1) / 2

        highest_num__layer_nodes = visual_helpers.get_highest_number_of_nodes(layers)

        variables = visual_helpers.optimize_variables(len(layers), highest_num__layer_nodes)

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
                x_coordinate = visual_helpers.get_coordinate(middle_layer_index, current_layer_index, length_between_layers, node_radius)
                y_coordinate = visual_helpers.get_coordinate(middle_node_index, current_node_index, length_between_nodes, node_radius)

                node = Circle(node_radius)

                node.move_to((x_coordinate, y_coordinate, 0))
                self.play(Create(node), run_time=0.1)

        self.wait(10)

    def receive_inputs(self):
        global inputs, hlayers, outputs
        variables = visual_helpers.receive_neural_network()
        inputs = variables[0]
        hlayers = variables[1]
        outputs = variables[2]


    def play_render(self):
        self.render()