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

        length_between_layers, length_between_nodes, node_radius = variables

        visual_helpers.generate_nodes(self, layers, middle_layer_index, length_between_layers, length_between_nodes, node_radius)

        self.wait(10)

    def receive_inputs(self):
        global inputs, hlayers, outputs
        variables = visual_helpers.receive_neural_network()
        inputs = variables[0]
        hlayers = variables[1]
        outputs = variables[2]


    def play_render(self, open_media_file = True):
        self.render()

        if open_media_file:
            open_file(self.renderer.file_writer.movie_file_path)


'''
To create a line between each node, we need to 
'''