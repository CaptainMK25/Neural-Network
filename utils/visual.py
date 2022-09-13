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


def round_variables(length_between_layers, length_between_nodes, node_radius):
    length_between_layers = round(length_between_layers, 2)
    length_between_nodes = round(length_between_nodes, 2)
    node_radius = round(node_radius, 2)

    return [length_between_layers, length_between_nodes, node_radius]


def optimize_variables(num_layers, num_layer_nodes):
    length_equation_for_length_between_layers = "(max_length-(2 * num_layers * node_radius))/(num_layers - 1)"
    length_equation_for_node_radius = "((-length_between_layers / 2) + ((length_between_layers + max_length)/(2 * num_layers)))"
    width_equation_for_length_between_nodes = "(max_width - (2 * num_layer_nodes * node_radius))/(num_layer_nodes - 1)"
    width_equation_for_node_radius = "(-length_between_nodes / 2) + ((max_width + length_between_nodes) / (2 * num_layer_nodes))"


    max_length = 6
    max_width = 3.5
    max_length_between_layers_constant = 1
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

    return round_variables(length_between_layers, length_between_nodes, node_radius)



test = [5, 1]
results = optimize_variables(test[0], test[1])
print(results)
print()
print(get_total_length(test[0], results[0], results[2]))
print(get_total_width(test[1], results[1], results[2]))