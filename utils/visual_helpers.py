from .importing import read_raw_parameters
from manim import *

def receive_neural_network():
    file = open("parameters.txt", mode="r")
    layers = read_raw_parameters(file.readlines())
    return layers

def get_total_number_nodes(layers):
    total = 0
    for layer in layers:
        total += len(layer)
        print(len(layer))

    return total

def adjust_coordinates_for_start_line(coordinates, node_radius):
    return [coordinates[0] + node_radius, coordinates[1], coordinates[2]]

def adjust_coordinates_for_end_line(coordinates, node_radius):
    return [coordinates[0] - node_radius, coordinates[1], coordinates[2]]

def generate_lines(visualize_object, coordinates_list, node_radius):
    for i in range(1, len(coordinates_list)):
        current_coordinates_layer = coordinates_list[i]

        for current_node_coordinates in current_coordinates_layer:
            previous_coordinates_layer = coordinates_list[i-1]

            for previous_node_coordinates in previous_coordinates_layer:
                adjusted_previous_node_coordinates = adjust_coordinates_for_start_line(previous_node_coordinates, node_radius)
                adjusted_current_node_coordinates = adjust_coordinates_for_end_line(current_node_coordinates, node_radius)
                line = Line(adjusted_previous_node_coordinates, adjusted_current_node_coordinates, color=YELLOW)
                visualize_object.play(Create(line), run_time = 0.1)


def generate_nodes_coordinates(visualize_object, layers, middle_layer_index, length_between_layers, length_between_nodes, node_radius):
    coordinates_list = []
    for current_layer_index in range(len(layers)):
        current_layer = layers[current_layer_index]
        middle_node_index = (len(current_layer) - 1) / 2

        current_layer_coordinates = []

        for current_node_index in range(len(current_layer)):
            x_coordinate = get_coordinate(middle_layer_index, current_layer_index, length_between_layers, node_radius)
            y_coordinate = get_coordinate(middle_node_index, current_node_index, length_between_nodes, node_radius)

            current_layer_coordinates.append([x_coordinate, y_coordinate, 0])

            node = Circle(node_radius)

            node.move_to((x_coordinate, y_coordinate, 0))
            visualize_object.play(Create(node), run_time=0.1)

        coordinates_list.append(current_layer_coordinates)

    return coordinates_list


def get_highest_number_of_nodes(layers):
    highest_num_nodes = 0
    for i in layers:
        current_num_nodes = len(i)
        if current_num_nodes > highest_num_nodes:
            highest_num_nodes = current_num_nodes

    return highest_num_nodes


def get_coordinate(middle_index, current_index, length, node_radius):
    difference_index = abs(middle_index - current_index)

    total = 0
    while difference_index > 0:
        if difference_index >= 1:
            total += length + (2 * node_radius)
            difference_index -= 1

        else:
            total += (length/2) + node_radius
            difference_index -= 0.5

    total = get_sign(middle_index, current_index) * total

    return total


def get_sign(middle_index, current_index):
    if middle_index > current_index:
        return -1

    else:
        return 1


def get_total_length(num_layers, length_between_layers, node_radius):
    total_length = (2 * num_layers * node_radius) + ((num_layers - 1) * length_between_layers)
    return total_length


def get_total_width(num_layer_nodes, length_between_nodes, node_radius):
    total_width = (2 * num_layer_nodes * node_radius) + ((num_layer_nodes - 1) * length_between_nodes)
    return total_width


def get_optimized_length(max_length_constant, max_length_equation):
    if (1.5 * max_length_constant) <= max_length_equation:
        return max_length_constant
    elif max_length_constant <= max_length_equation:
        return 0.5 * max_length_equation
    else:
        return 0.7 * max_length_equation


def round_dimensions_variables(length_between_layers, length_between_nodes, node_radius):
    length_between_layers = round(length_between_layers, 2)
    length_between_nodes = round(length_between_nodes, 2)
    node_radius = round(node_radius, 2)

    return [length_between_layers, length_between_nodes, node_radius]


def optimize_variables(num_layers, num_layer_nodes):
    length_equation_for_length_between_layers = "(max_length-(2 * num_layers * node_radius))/(num_layers - 1)"
    length_equation_for_node_radius = "((-length_between_layers / 2) + ((length_between_layers + max_length)/(2 * num_layers)))"
    width_equation_for_length_between_nodes = "(max_width - (2 * num_layer_nodes * node_radius))/(num_layer_nodes - 1)"
    width_equation_for_node_radius = "(-length_between_nodes / 2) + ((max_width + length_between_nodes) / (2 * num_layer_nodes))"


    max_length = 12
    max_width = 6
    max_length_between_layers_constant = 1.5
    max_length_between_nodes_constant = 0.5

    node_radius = 0

    max_length_between_layers_equation = eval(length_equation_for_length_between_layers)

    length_between_layers = get_optimized_length(max_length_between_layers_constant, max_length_between_layers_equation)

    node_radius = eval(length_equation_for_node_radius)

    if get_total_width(num_layer_nodes, max_length_between_nodes_constant, node_radius) > max_width:
        node_radius = 0
        max_length_between_nodes_equation = eval(width_equation_for_length_between_nodes)
        length_between_nodes = get_optimized_length(max_length_between_nodes_constant, max_length_between_nodes_equation)

        node_radius = eval(width_equation_for_node_radius)

    else:
        length_between_nodes = max_length_between_nodes_constant

    return round_dimensions_variables(length_between_layers, length_between_nodes, node_radius)



'''
total_run_time = (number of nodes + number of lines) * run_time

run_time = (total_run_time)/(number of nodes + number of lines)

We will ignore the number of lines for simplicity

run time = (total run time)/(number of nodes)

We set total run time to a constant, and we always have access to the number of nodes, so we can calculate the run time
'''