import numpy as np

def evaluate_neural_network_outputs(layers, activation_function):
    '''
    Evaluates the current neural network with given inputs, weights and biases and an activation function. Returns the final output of the neural network's output nodes

    Parameters
    ----------
    layers: list
        List of ndarrays containing each layer's nodes
    activation_function: str
        Name of the activation function to be used by the neural network
    '''

    inputs = layers[0]

    for layer_index in range(1, len(layers)):
        current_layer = layers[layer_index]

        # current_layer is a matrix with rows as node's parameters (weights and bias)

        # To extract the bias and weights, slice the array
        biases = current_layer[:,-1]
        weights = current_layer[:,:-1]

        # Transpose the weights to have each column represent a node, since the inputs matrix is horizontal

        transposed_weights = np.transpose(weights)

        output = np.matmul(inputs, transposed_weights) + biases  # type: ignore

        # Activating the nodes producing the current output
        activated_output = activate_output(output, activation_function)
        
        # Making the output the input for the next layer
        inputs = activated_output

    # Since we're last updating the inputs variables to hold the final outputs of the output layer, it should be returned
    return inputs


def activate_output(output, activation_function):
    '''
    Activates the output at each layer of nodes using a given activation function

    Parameters
    ----------
    output: ndarray
        1D numpy array containing the current layer's outputs to be activated
    activation_function: str
        Name of the activation function to be used by the neural network
    '''
    for index in range(len(output)):
        current_output = output[index]

        if activation_function == "relu":
            output[index] = reLU_function(current_output)
        elif activation_function == "sigmoid":
            output[index] = sigmoid_function(current_output)
        elif activation_function == "binary":
            output[index] = binary_function(current_output)
        elif activation_function == "linear":
            output[index] =  output[index]

    return output



def reLU_function(current_output):
    '''
    Returns the value of the reLU function evaluated at current_output

    Parameters
    ----------
    current_output: float
        The output value of a certain node in a certain layer to be activated
    '''
    if current_output > 0:
        return current_output
    else:
        return 0

def sigmoid_function(current_output):
    '''
    Returns the value of the sigmoid function evaluated at current_output

    Parameters
    ----------
    current_output: float
        The output value of a certain node in a certain layer to be activated
    '''

    result = 1 / (1 + (np.e ** (-current_output)))
    return result

def binary_function(current_output):
    '''
    Returns the value of the binary function evaluated at current_output

    Parameters
    ----------
    current_output: float
        The output value of a certain node in a certain layer to be activated
    '''
    
    if current_output >=0:
        return 1
    else:
        return 0

