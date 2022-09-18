def create_inputs_string(inputs):
	inputs_string = "i\n"
	for i in inputs:
			inputs_string += str(i) + " "

	return inputs_string + "\n"


def create_hlayers_string(hlayers):
		hlayers_string = ""
		for i in hlayers:
				hlayers_string += "h\n"
				for j in i:
					for k in j:
						hlayers_string += str(k) + " "
					
					hlayers_string += "\n"

		return hlayers_string


def create_outputs_string(outputs):
	outputs_string = "o\n"
	for i in outputs:
		for j in i:
			outputs_string += str(j) + " "

	return outputs_string


def create_paramters_string(inputs, outputs, hlayers = []):
	parameters = create_inputs_string(inputs)

	if hlayers != []:
		parameters += create_hlayers_string(hlayers)

	parameters += create_outputs_string(outputs)

	return parameters