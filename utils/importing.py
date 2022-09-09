import numpy as np

def check_valid(raw_parameters):
    inputs = []
    hlayers = []
    outputs = []

    current_hlayer = []

    num_inputs = 0
    num_outputs = 0
    num_output_parameters = 0
    num_hlayer_nodes = 0

    count = 0

    read_input = False
    read_output = False

    
    for i in range(len(raw_parameters)):
        current_value = read_element(raw_parameters[i])

        if current_value == "input" and read_input:
            return False
        elif current_value == "input":
            read_input = True
            try:
                inputs = read_element(raw_parameters[i+1])
                num_inputs = len(inputs)
            except:
                return False


        if current_value == "output" and read_output:
            return False
        elif current_value == "output":
            read_output = True
            try:
                count = i + 1
                while count < len(raw_parameters):
                    current_value = read_element(raw_parameters[count])
                    outputs.append(current_value)
                    count += 1

                num_outputs = len(outputs)

            except:
                return False

        if current_value == "hlayer":
            count = i + 1
            while type(read_element(raw_parameters[count])) == list:
                current_value = read_element(raw_parameters[count])
                current_hlayer.append(current_value)
                count += 1

            hlayers.append(current_hlayer)
            
    for i in range(len(outputs)):
        if i == 0:
            num_output_parameters = len(outputs[0])
            if num_output_parameters != len(hlayers[len(hlayers)-1]) + 1:
                return False

        else:
            current_num_output_parameters = len(outputs[i])

            if current_num_output_parameters != num_output_parameters:
                return False

    
    
    for i in range(len(hlayers)):
        if i == 0:
            hlayer1 = hlayers[0]
            num_hlayer_nodes = len(hlayer1)
            num_hlayer_node_parameters = len(hlayer1[0])

            if num_hlayer_node_parameters != num_inputs + 1:
                return False

            for i in hlayer1:
                if len(i) != num_hlayer_node_parameters:
                    return False

        else:
            current_hlayer = hlayers[i]
            current_num_hlayer_nodes = len(current_hlayer)
            num_hlayer_node_parameters = len(current_hlayer[0])

            if current_num_hlayer_nodes != num_hlayer_nodes:
                return False

            if num_hlayer_node_parameters != num_hlayer_nodes + 1:
                return False

            for i in current_hlayer:
                if len(i) != num_hlayer_node_parameters:
                    return False

        if i == len(hlayers) - 1:
            last_hlayer = hlayers[i]
            last_hlayer_nodes = len(last_hlayer)
            if num_outputs != last_hlayer_nodes + 1:
                return False


    return [inputs, hlayers, outputs]



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
        return node_parameter_values
