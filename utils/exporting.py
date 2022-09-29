def create_inputs_string(inputs):
	"""
	Creates the string of inputs to be written in the exported .txt file

	Parameters
	----------
	inputs: ndarray
		1D array containing input values from the neural network
	"""
	inputs_string = "i\n"
	for i in inputs:
			inputs_string += str(i) + " "

	return inputs_string + "\n"


def create_hlayers_string(hlayers):
	"""
	Creates the string of hidden layers to be written in the exported .txt file

	Parameters
	----------
	hlayers: ndarray
		3D array containing each hidden layer and their nodes' values from the neural network
	"""
	hlayers_string = ""
	for i in hlayers:
		hlayers_string += "h\n"
		for j in i:
			for k in j:
				hlayers_string += str(k) + " "

			hlayers_string += "\n"

	return hlayers_string


def create_outputs_string(outputs):
	"""
	Creates the string of outputs to be written in the exported .txt file

	Parameters
	----------
	outputs: ndarray
		2D array containing output nodes' values from the neural network
	"""
	outputs_string = "o\n"
	for i in outputs:
		for j in i:
			outputs_string += str(j) + " "
		outputs_string += "\n"

	

	return outputs_string


def create_parameters_string(inputs, outputs, hlayers):
	"""
	Creates the parameters string to be written in the exported .txt file

	Parameters
	----------
	inputs: ndarray
		1D array containing input values from the neural network
	hlayers: ndarray
		3D array containing each hidden layer and their nodes' values from the neural network
	outputs: ndarray
		2D array containing output nodes' values from the neural network
	"""
	parameters = create_inputs_string(inputs)

	if hlayers != []:
		parameters += create_hlayers_string(hlayers)

	parameters += create_outputs_string(outputs)

	return parameters