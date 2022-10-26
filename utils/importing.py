import numpy as np

def import_parameters(raw_parameters):
    '''
    Parses the raw_parameters list, reforms it into a neural network structure, checks if it's a valid structure, then restructure the lists inside it to organized numpy arrays and returns them. If the structure is not valid, it returns False

    Parameters
    ----------
    raw_parameters: list
        List of the lines in the {name}.txt file
    '''
    parsed_parameters = parse_raw_parameters(raw_parameters)

    if (check_import_validity(parsed_parameters)):
        return reconstruct_import(parsed_parameters)

    else:
        return False

def import_parameters_for_visualization(raw_parameters):
    '''
    Parses the raw_parameters and reforms into a neural network structure, then groups the layers together in a list and returns that
    This is a specialized method, and it's guaranteed to be importing a valid structure

    Parameters
    ----------
    raw_parameters: list
        List of the lines in the parameters.txt file
    '''
    parsed_parameters = parse_raw_parameters(raw_parameters)

    layers = []
    inputs = parsed_parameters[0]  # type: ignore
    hlayers = parsed_parameters[1]  # type: ignore
    outputs = parsed_parameters[2]  # type: ignore

    inputs = inputs[0][0]

    outputs = outputs[0]

    layers.append(inputs)
    layers.append(hlayers)
    layers.append(outputs)
    return layers



def parse_raw_parameters(raw_parameters):
    '''
    Parses the raw_parameters list and reforms it into a neural network structure. Returns a neural network structure if the raw_parameters list has a valid format, False otherwise

    Parameters
    ----------
    raw_parameters: list
        List of the lines in the {name}.txt file
    '''

    result_neural_network_structure = []

    inputs = []
    hlayers = []
    outputs = []

    index = 0

    while index < len(raw_parameters):
        current_line = raw_parameters[index]
        current_line_value = parse_line(current_line)

        if current_line_value == False:
            return False
        

        elif type(current_line_value) == str:
            index += 1

            index, current_parsed_section = parse_layer_section(index, raw_parameters)

            if current_line_value == "input":
                inputs.append(current_parsed_section)

            elif current_line_value == "hlayer":
                hlayers.append(current_parsed_section)

            elif current_line_value == "output":
                outputs.append(current_parsed_section)

            else:
                return False

    result_neural_network_structure.append(inputs)
    result_neural_network_structure.append(hlayers)
    result_neural_network_structure.append(outputs)

    return result_neural_network_structure



def check_import_validity(parsed_parameters):
    '''
    Returns True if the given parsed_parameters is a valid neural network structure, False otherwise

    Parameters
    ----------
    parsed_parameters: list
        List of the parsed parameters provided by the parse_parameters function

    Validity Requirements
    ---------------------
    - Only 1 input layer
    - Only 1 node in the input layer
    - Only 1 output layer
    - Number of inputs = number of first hlayer first node parameters - 1
    - Number of hlayer nodes = number of first output node parameters - 1
    - All hidden layer nodes have the same number of nodes
    - All first hidden layer nodes have the same number of parameters per node
    - All second and above hidden layer have the same number of parameters per node
    - If there's no hidden layers, number of inputs = number of parameters for first node in outputs - 1
    - All output nodes have the same number of parameters
    '''

    # Checking that the parameter parsing was successfull
    if parsed_parameters == False:
        return False

    inputs = parsed_parameters[0]
    hlayers = parsed_parameters[1]
    outputs = parsed_parameters[2]

    # Checking that there's only one inputs section
    if len(inputs) != 1:
        return False

    # Reducing inputs to the single inputs layer
    inputs = inputs[0]

    # Checking that the inputs layer has only one node (i.e one line of values)
    if len(inputs) != 1:
        return False

    # Reducing inputs to the list of input values
    inputs = inputs[0]

    # Checking that there are input values
    if len(inputs) == 0:
        return False


    # Checking that there's only one outputs section
    if len(outputs) != 1:
        return False

    # Reducing outputs to the single outputs layer
    outputs = outputs[0]


    # Checking that there's at least one output node
    if len(outputs) == 0:
        return False


    number_of_inputs = len(inputs)
    first_output_node = outputs[0]

    number_of_output_parameters = len(first_output_node)

    # In the case that there are hidden layers in this structure
    if len(hlayers) != 0:
        first_hlayer = hlayers[0]

        # Checking that the hidden layer is not empty
        if len(first_hlayer) == 0:
            return False

        first_node_first_hlayer = first_hlayer[0]

        # Checking that the number of inputs is equal to the number of parameters (weights) for a node in the hidden layers minus one parameter for the bias
        if number_of_inputs != len(first_node_first_hlayer) - 1:
            return False

        last_hlayer = hlayers[-1]

        # Checking that the number of nodes in a hidden layer is equal to the number of parameters of a node in the outputs minus the bias
        if len(last_hlayer) != number_of_output_parameters - 1:
            return False

        # Checking that all hidden layers' nodes have the same number of parameters
        if not check_hlayers_validity(hlayers):
            return False

    # In the case that there aren't hidden layers in this structure
    else:
        # Checking that the number of inputs is equal to the number of parameters of a node in the outputs minus the bias
        if number_of_inputs != len(first_output_node) - 1:
            return False

    # Checking that all output nodes have the same number of parameters
    if not check_outputs_validity(outputs):
        return False


    return True               


def check_hlayers_validity(hlayers):
    '''
    Returns True if the provided hidden layers is valid, False otherwise

    Parameters
    ----------
    hlayers: list
        List of the hidden layers parsed by the parse_parameters function

    Validity Requirements
    ---------------------
    - All hidden layer nodes have the same number of nodes
    - All first hidden layer nodes have the same number of parameters per node
    - All second and above hidden layer have the same number of parameters per node
    '''

    number_of_nodes = len(hlayers[0])

    first_node_first_hlayer_number_of_parameters = len(hlayers[0][0])

    if len(hlayers) > 1:
        first_node_second_hlayer_number_of_parameters = len(hlayers[1][0])
    else:
        first_node_second_hlayer_number_of_parameters = 0

    count = 0

    for layer in hlayers:
        if count == 0:
            for node in layer:
                if len(node) != first_node_first_hlayer_number_of_parameters:
                    return False

        else:
            for node in layer:
                if len(node) != first_node_second_hlayer_number_of_parameters:
                    return False

        if len(layer) != number_of_nodes:
            return False

        count += 1

    return True


def check_outputs_validity(outputs):
    '''
    Returns True if the provided outputs is valid, False otherwise

    Parameters
    ----------
    outputs: list
        List of the outputs provided by the parse_parameters function

    Validity Requirements
    ---------------------
    - All output nodes have the same number of parameters
    '''

    number_of_parameters_of_first_node_in_outputs = len(outputs[0])

    for node in outputs:
        if len(node) != number_of_parameters_of_first_node_in_outputs:
            return False

    return True


def parse_layer_section(current_index, raw_parameters):
    '''
    Parses the layer/section in the raw_parameters list indicated by the current index. Returns the index after parsing the section and the resulting parsed section

    Parameters
    ----------
    current_index: int
        Indicated the index of the start of the layer/section to parse
    raw_parameters: list
        List of the lines in the {name}.txt file
    '''
    index = current_index
    result = []
    while True:
        if index < len(raw_parameters):
            current_line = raw_parameters[index]
            current_line_value = parse_line(current_line)

            if type(current_line_value) == list:
                result.append(current_line_value)
                index += 1
            else:
                break

        else:
            break

    return index, result



def reconstruct_import(valid_parameters):
    '''
    Reconstructs the parsed and valid parameters list into the three needed variables, inputs (numpy array), hlayers (list of numpy arrays) and outputs (numpy arrays)

    Parameters
    ----------
    valid_parameters: list
        List of valid parameters parsed by the parse_parameters and checked by the check_import_validity function
    '''
    inputs = valid_parameters[0]
    hlayers = valid_parameters[1]
    outputs = valid_parameters[2]

    inputs = np.array(inputs[0][0])
    hlayers = [np.array(layer) for layer in hlayers]
    outputs = np.array(outputs[0])

    return inputs, hlayers, outputs



def parse_line(line):
    '''
    Parses a single line of the raw_parameters list. Returns "input"/"hlayer"/"output" if the line indicates the start of a section "i"/"h"/"o", or a list of the values in the line. It returns False otherwise

    Parameters
    ----------
    line: str
        String of the line in the raw_parameters list of lines
    '''
    if line[0] == "i":
        return "input"

    elif line[0] == "h":
        return "hlayer"

    elif line[0] == "o":
        return "output"

    else:
        try:
            # Removes /n character and splits line into a string of parameters
            node_parameter_values = line[:-1].strip().split(" ")
            # Changing all parameters data types to integer
            node_parameter_values = [float(i) for i in node_parameter_values]
            return node_parameter_values
        except:
            return False


