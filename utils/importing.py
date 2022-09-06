import numpy as np

def read_element(line):
    if line[0] == "i":
        return "input"

    elif line[0] == "h":
        return "hlayer"

    elif line[0] == "o":
        return "output"

    else:
        node_parameter_values = line[:-1].strip().split(" ")
        node_parameter_values = [int(i) for i in node_parameter_values]
        return np.array(node_parameter_values)


def set_mode(value, current_mode):
    status = "unchanged"
    if type(value) == str:
        status = "changed"
        return [value, status]

    else:
        return [current_mode, status]
            

def read_parameters(parameters):
    single_hlayer = []
    inputs = []
    hlayers = []
    outputs = []
    current_mode = ""
    for i in parameters:
        current_value = read_element(i)

        mode_status = set_mode(current_value, current_mode)
        current_mode = mode_status[0]
        status = mode_status[1]


        if status == "changed" and single_hlayer != []:
            hlayers.append(np.array(single_hlayer))
            single_hlayer = []

        if type(current_value).__module__ == np.__name__:
            if current_mode == "input":
                inputs = np.array(current_value)

            elif current_mode == "hlayer":
                single_hlayer.append(np.array(current_value))

            elif current_mode == "output":
                outputs.append(np.array(current_value))


    return [np.array(inputs), hlayers, np.array(outputs)]