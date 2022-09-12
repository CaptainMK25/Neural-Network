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
    total_length = (num_layers * node_radius) + ((num_layers - 1) * length_between_layers)
    return total_length


def get_total_width(num_layer_nodes, length_between_nodes, node_radius):
    total_width = (num_layer_nodes * node_radius) + ((num_layer_nodes - 1) * length_between_nodes)
    return total_width


'''
2 options:
- Inefficient, lazy, 0 quality way: We try a set of x,y,z numbers, if it doesn't work, modify them correspondingly

- Hard, painful way: Get a list of x,y,z values in a dictionary, and for each interval of length and width, give the corresponding x,y,z values

'''

'''
length between layers: x
length between nodes: y
radius: z

num layers = a
num layer node = b

We want to optimize 2 of the three variables first, then set them as fixed constants and optimize the third variable, we'll start with optimizing the length with x and z:

'''