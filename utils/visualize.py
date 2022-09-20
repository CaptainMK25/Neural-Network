from manim import *
import numpy as np
from .visual_helpers import *

class VisualizeNeuralNetwork(Scene):

    def construct(self):
        layers = hlayers
        layers.insert(0, [[i] for i in inputs])
        layers.append(outputs)
        middle_layer_index = (len(layers) - 1) / 2
        highest_num_layer_nodes = get_highest_number_of_nodes(layers)
        total_number_nodes = get_total_number_nodes(layers)

        total_run_time = 5

        variables = optimize_variables(len(layers), highest_num_layer_nodes)
        length_between_layers, length_between_nodes, node_radius = variables

        coordinates_list = generate_nodes_coordinates(self, layers, middle_layer_index, length_between_layers, length_between_nodes, node_radius, total_number_nodes, total_run_time)

        generate_lines(self, coordinates_list, node_radius, total_number_nodes, total_run_time)

        self.wait(2)


    def receive_inputs(self):
        global inputs, hlayers, outputs
        variables = receive_neural_network()
        inputs, hlayers, outputs = variables


    def play_render(self, open_media_file = True):
        self.render()

        if open_media_file:
            open_file(self.renderer.file_writer.movie_file_path)
