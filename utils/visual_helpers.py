from .importing import import_parameters_for_visualization
from manim import *

def get_node_run_time(total_number_nodes, total_run_time):
    '''
    Returns the required run time for a single node

    Parameters
    ----------
    total_number_nodes: int
        The total number of nodes in the neural network
    total_run_time: int
        The total run time required for the video
    '''
    total_node_run_time = total_run_time / 2
    run_time_one_node = total_node_run_time / total_number_nodes
    return run_time_one_node


def get_line_run_time(total_number_nodes, total_run_time):
    '''
    Returns approximately the required run time for a single line

    Parameters
    ----------
    total_number_nodes: int
        The total number of nodes in the neural network
    total_run_time: int
        The total run time required for the video
    '''
    total_line_run_time = total_run_time / 2
    run_time_one_line = total_line_run_time / (total_number_nodes ** 2)
    return run_time_one_line


def get_line_width(total_number_nodes):
    '''
    Returns the required line width to fit the overall neural network look

    Parameters
    ----------
    total_number_nodes: int
        The total number of nodes in the neural network
    '''
    width = 1
    if total_number_nodes < 25:
        width = -0.15 * (total_number_nodes - 2) + 5

    return width


def get_total_number_nodes(layers):
    '''
    Returns the total number of nodes in the neural network

    Parameters
    ----------
    layers: list
        The layers of the neural network, filled with nodes
    '''
    total_number_nodes = 0
    for layer in layers:
        total_number_nodes += len(layer)

    return total_number_nodes


def adjust_coordinates_for_start_line(coordinates, node_radius):
    '''
    Returns the adjusted position of the line to the right to fit with the outgoing node

    Parameters
    ----------
    coordinates: list
        List of the coordinates of the outgoing node
    node_radius: int
        Radius of the outgoing node
    '''
    return np.array([coordinates[0] + node_radius, coordinates[1], coordinates[2]])


def adjust_coordinates_for_end_line(coordinates, node_radius):
    '''
    Returns the adjusted position of the line to the left to fit with the incoming node

    Parameters
    ----------
    coordinates: list
        List of the coordinates of the incoming node
    node_radius: int
        Radius of the incoming node
    '''
    return np.array([coordinates[0] - node_radius, coordinates[1], coordinates[2]])


def generate_lines(visualize_object, coordinates_list, node_radius, total_number_nodes, total_run_time):
    '''
    Generates the lines from each node in each layer to each node in the following layer
    
    Parameters
    ----------
    visualize_object: VisualizeNeuralNetwork
        VisualizeNeuralNetwork object used to add the Manim animated objects to the scene to be rendered
    coordinates_list: List
        List of the coordinates for each layer, which is a list of the coordinates every node in the layer
    node_radius: int
        The node radius for every node in the video
    total_number_nodes: int
        The total number of nodes in the neural network
    total_run_time: int
        The total run time required for the video
    '''

    run_time_one_line = get_line_run_time(total_number_nodes, total_run_time)

    for i in range(1, len(coordinates_list)):
        current_coordinates_layer = coordinates_list[i]

        for current_node_coordinates in current_coordinates_layer:
            previous_coordinates_layer = coordinates_list[i-1]

            for previous_node_coordinates in previous_coordinates_layer:
                adjusted_previous_node_coordinates = adjust_coordinates_for_start_line(previous_node_coordinates, node_radius)
                adjusted_current_node_coordinates = adjust_coordinates_for_end_line(current_node_coordinates, node_radius)
                line = Line(adjusted_previous_node_coordinates, adjusted_current_node_coordinates, color=YELLOW)
                line.stroke_width = get_line_width(total_number_nodes)
                visualize_object.play(Create(line), run_time=run_time_one_line)


def generate_nodes_coordinates(visualize_object, layers, middle_layer_index, length_between_layers, length_between_nodes, node_radius, total_number_nodes, total_run_time):
    '''
    Generates the nodes and adds them to the scene to be rendered. Generates their coordinates list and returns it

    Parameters
    ----------
    visualize_object: VisualizeNeuralNetwork
        VisualizeNeuralNetwork object used to add the Manim animated objects to the scene to be rendered
    layers: list
        List of the layers (inputs, hlayers, outputs) of the neural network
    middle_layer_index: int
        The index of the layer in the middle of the neural network
    length_between_layers: int
        The required length between every layer to maximize the size of the rendered objects
    length_between_nodes: int
        The required length between every two nodes vertically to maximize the size of the rendered objects
    node_radius: int
        The node radius for every node in the video
    total_number_nodes: int
        The total number of nodes in the neural network
    total_run_time: int
        The total run time required for the video
    '''

    run_time_one_node = get_node_run_time(total_number_nodes, total_run_time)
    
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
            visualize_object.play(Create(node), run_time=run_time_one_node)

        coordinates_list.append(current_layer_coordinates)

    return coordinates_list


def get_highest_number_of_nodes(layers):
    '''
    Returns the highest number of nodes in a single layer

    Parameters
    ----------
    layers: list
        List of the layers (inputs, hlayers, outputs) of the neural network
    '''
    highest_num_nodes = 0
    for i in layers:
        current_num_nodes = len(i)
        if current_num_nodes > highest_num_nodes:
            highest_num_nodes = current_num_nodes

    return highest_num_nodes


def get_coordinate(middle_index, current_index, length, node_radius):
    '''
    Returns the needed coordinate for the given node characteristics

    Parameters
    ----------
    middle_index: int
        The index of the layer in the middle of the neural network
    current_index: int
        The index of the current node's layer
    length: int
        The length between layers or nodes if we're getting the x or y coordinate respectively
    node_radius: int
        The node radius for every node in the video
    '''
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
    '''
    Returns the sign of the coordinate depending on the position of the current node. Left to the middle is a negative sign, right to the middle is a positive sign

    Parameters
    ----------
    middle_index: int
        The index of the layer in the middle of the neural network
    current_index: int
        The index of the current node's layer
    '''
    if middle_index > current_index:
        return -1

    else:
        return 1


def get_total_length(num_layers, length_between_layers, node_radius):
    '''
    Returns the total length of the whole neural network based on the given dimensions

    Parameters
    ----------
    num_layers: int
        Number of layers in the neural network
    length_between_layers: int
        The required length between every layer
    node_radius: int
        The node radius for every node in the video
    '''
    total_length = (2 * num_layers * node_radius) + ((num_layers - 1) * length_between_layers)
    return total_length


def get_total_width(num_layer_nodes, length_between_nodes, node_radius):
    '''
    Returns the total width of the whole neural network based on the given dimensions

    Parameters
    ----------
    num_layers_nodes: int
        Number of nodes in the current layer
    length_between_nodes: int
        The required length between every two nodes vertically
    node_radius: int
        The node radius for every node in the video
    '''
    total_width = (2 * num_layer_nodes * node_radius) + ((num_layer_nodes - 1) * length_between_nodes)
    return total_width


def get_optimized_length(max_length_constant, max_length_equation):
    '''
    Returns the maximized length between layers or nodes, based on the given optimizing equations

    Parameters
    ----------
    max_length_constant: int
        The maximum length between layers or nodes to avoid having awkwardly big elements
    max_length_equation: int
        Result of the length equation for length between layers or between nodes
    '''
    if (1.5 * max_length_constant) <= max_length_equation:
        return max_length_constant
    elif max_length_constant <= max_length_equation:
        return 0.5 * max_length_equation
    else:
        return 0.7 * max_length_equation


def round_dimensions_variables(length_between_layers, length_between_nodes, node_radius):
    '''
    Returns a list of the three given numbers rounded to 2 decimal places

    Parameters
    ----------
    length_between_layers: int
        The required length between every layer
    length_between_nodes: int
        The required length between every two nodes vertically
    node_radius: int
        The node radius for every node in the video
    '''
    length_between_layers = round(length_between_layers, 2)
    length_between_nodes = round(length_between_nodes, 2)
    node_radius = round(node_radius, 2)

    return [length_between_layers, length_between_nodes, node_radius]


def optimize_variables(num_layers, highest_num_layer_nodes):
    '''
    Returns maximized length between layers, between nodes and node radius, to scale the neural network as much as possible in the video

    Parameters
    ----------
    num_layers: int
        The number of layers in the neural network
    highest_num_layer_nodes: int
        The highest number of nodes in a layer
    '''
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

    if get_total_width(highest_num_layer_nodes, max_length_between_nodes_constant, node_radius) > max_width:
        node_radius = 0
        max_length_between_nodes_equation = eval(width_equation_for_length_between_nodes)
        length_between_nodes = get_optimized_length(max_length_between_nodes_constant, max_length_between_nodes_equation)

        node_radius = eval(width_equation_for_node_radius)

    else:
        length_between_nodes = max_length_between_nodes_constant

    return round_dimensions_variables(length_between_layers, length_between_nodes, node_radius)