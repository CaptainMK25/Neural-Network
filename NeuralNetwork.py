import numpy as np
import os
import utils.importing as importing
import utils.exporting as exporting
import utils.visualize as visualize
import utils.evaluation as evaluation

class NeuralNetwork():
	"""
	A class used to represent a Neural Network

	Attributes
	----------
	num_inputs: int
		Number of input nodes in the neural network
	num_hlayers: int
		Number of hidden layers in the neural network
	num_hlayers_nodes: int
		Number of nodes in each hidden layer in the neural network
	num_outputs: int
		The number of outputs in the neural network

	inputs: ndarray
		1D array containing input nodes values of type `float`
	hlayers: List
		3D array containing the hidden layers of type ndarray, which contains hidden layers' nodes of type ndarray, which contains hidden layers' nodes' values of type float
		Example: 2 hidden layers with 2 nodes each with 3 input nodes
			hlayers = [hidden layer: ndarray([node values: ndarray([0.0, 0.0, 0.0, 0.0]), node values: ndarray([0.0, 0.0, 0.0, 0.0])]),
					   hidden layer: ndarray(node values: ndarray([0.0, 0.0, 0.0]), node values: ndarray([0.0, 0.0 0.0]))]
			hlayers = [ndarray(ndarray([0.0, 0.0, 0.0, 0.0]), ndarray([0.0, 0.0, 0.0, 0.0])),
					   ndarray([ndarray(0.0, 0.0, 0.0), ndarray([0.0, 0.0, 0.0])])]
	outputs: ndarray
		2D array containing the output nodes of type ndarray, which contains each output node's values of type float
	layers: list
		3D array containing the inputs, hlayers and outputs as equal layers, stored in the same list hierarchy

	activation_function: str
		String of the name of the activation function to be used by the neural network
		Set to "reLU" by default

	
	Methods
	-------
	get_inputs()
		Returns the inputs ndarray of the neural network
	get_hlayers()
		Returns the hidden layers' list of the neural network
	get_outputs()
		Returns the output ndarray of the neural network
	export_parameters(name="parameters", message=True)
		Exports neural network node parameters to a .txt file in the same directory
	import_parameters(override_structure=True, name="parameters", message=True)
		Imports neural network node parameters from a .txt file in the same directory
	visualize(open_media_file=True)
		Renders a video of the neural network's node and connections

	"""
	def __init__(self, num_inputs = 1, num_outputs = 1, num_hlayers = 0, num_hlayer_nodes = 1):
		"""
		Parameters
		----------
		num_inputs: int, optional
			Number of input nodes in the neural network
		num_hlayers: int, optional
			Number of hidden layers in the neural network
		num_hlayers_nodes: int, optional
			Number of nodes in each hidden layer in the neural network
		num_outputs: int, optional
			The number of outputs in the neural network
		"""
		self.num_inputs = num_inputs
		self.num_hlayers = num_hlayers
		self.num_hlayers_nodes = num_hlayer_nodes
		self.num_outputs = num_outputs

		self.inputs = np.array([0.0 for i in range(num_inputs)], ndmin=1)


		if num_hlayers >= 1 and num_hlayer_nodes > 0:
			hlayer1_node_vector = [0.0 for i in range(num_inputs + 1)]
			hlayer1 = [hlayer1_node_vector for i in range(num_hlayer_nodes)]
			hlayer1 = np.array(hlayer1, ndmin=2)

			hlayers_node_vector = [0.0 for i in range(num_hlayer_nodes + 1)]
			other_hlayers = [hlayers_node_vector for j in range(num_hlayer_nodes)]
			other_hlayers = np.array(other_hlayers, ndmin=2)

			hlayers = [hlayer1]
			for i in range(1, num_hlayers):
				hlayers.append(other_hlayers)


			self.hlayers = hlayers

			last_hlayer_length = len(self.hlayers[len(self.hlayers) - 1])

			outputs_node_vector = [0.0 for i in range(last_hlayer_length + 1)]
			outputs = [outputs_node_vector for i in range(num_outputs)]
			self.outputs = np.array(outputs, ndmin=2)

		else:
			self.hlayers = []
			self.num_hlayers_nodes = 0
			outputs_node_vector = [0.0 for i in range(num_inputs)]
			outputs = [outputs_node_vector for i in range(num_outputs)]
			self.outputs = np.array(outputs, ndmin=2)

		self.generate_layers()

		self.activation_function = "relu"


	def get_inputs(self):
		"""
		Returns the inputs ndarray of the neural network
		"""
		return self.inputs


	def get_hlayers(self):
		"""
		Returns the hidden layers' list of the neural network
		"""
		if self.num_hlayers >= 1:
			return self.hlayers

		else:
			return None


	def get_outputs(self):
		"""
		Returns the outputs ndarray of the neural network
		"""
		return self.outputs


	def get_layers(self):
		'''
		Returns the layers list containing all the layers of the neural network
		'''
		return self.layers

	def get_activation_function(self):
		'''
		Returns the activation function used by the neural network
		'''
		return self.activation_function

	def set_activation_function(self, new_activation_function):
		'''
		Sets a new activation function to be used by the neural network. Supported activation functions:\n
		-reLU\n
		-Sigmoid\n
		-Binary\n
		-Linear\n

		Parameters
		----------
		new_activation_function: str
			Name of the new activation function to be used by the neural network

		Warnings
		--------
		For regression, the best activation function is linear
		For classification, the best activation function is sigmoid

		The reLU may lead to the dying reLU problem, which happens when an input to a node is always negative, so the node never gets activated and therefore, never learns\n
		The sigmoid may lead to very slow learning rates when used with large inputs, since the sigmoid function flattens with greater values\n
		The binary is too simple and may lead to a network that can never fit more complex problems\n
		The linear is, as the name suggests, always linear so it leads to a linear neural network output and may not fit more complex problems
		'''

		new_activation_function_name = new_activation_function.strip().lower()

		if new_activation_function_name == "relu":
			self.activation_function = "relu"
		elif new_activation_function_name == "sigmoid":
			self.activation_function = "sigmoid"
		elif new_activation_function_name == "binary":
			self.activation_function = "binary"
		elif new_activation_function_name == "linear":
			self.activation_function = "linear"
		else:
			print("Unsupported activation function. Set to default: reLU")


	def generate_layers(self):
		'''
		Generates the layers list containing all the layers of the neural network
		'''
		layers = self.hlayers
		layers.insert(0, self.inputs)
		layers.append(self.outputs)

		self.layers = layers

	


	def export_parameters(self, name="parameters", message=True):
		"""
		Exports the parameters of the neural network to a {name}.txt file, and indicates the status of the export if message is True

		Parameters
		----------
		name: str, optional
			The name of the text file to export to, (default is "parameters")
		message: bool, optional
			Prints an indicator message to the user if True (default is True)
		"""
		export_file = open(name + ".txt", mode="w")

		export_file.write(exporting.create_parameters_string(self.inputs, self.outputs, self.hlayers))

		export_file.close()

		if message:
			print("Export Successful")


	def import_parameters(self, override_structure=True, name="parameters"):
		"""
		Imports the parameters of the neural network from a {name}.txt file, and indicates the status of the import if message is True

		Parameters
		----------
		override_structure: bool, optional
			If True, the import will completely rewrite the current network's structure to the given {name}.txt file. If False, the import will not pass unless the given structure from {name}.txt corresponds to the current network structure, (default is True)
		name: str, optional
			The name of the text file to import from, (default is "parameters")

		Raises
		------
		OSError
			If the given file name is not found in the same directory
		"""
		try:
			import_file = open(name + ".txt", mode="r")
		except:
			raise OSError(f"file {name}.txt not found")

		raw_parameters = import_file.readlines()

		valid_parsed_parameters = importing.import_parameters(raw_parameters)

		if valid_parsed_parameters == False:
			print("Import Error, imported network is invalid")
			return None

		inputs, hlayers, outputs = valid_parsed_parameters

		imported_num_inputs = np.size(inputs)
		imported_num_hlayers = len(hlayers)
		if imported_num_hlayers == 0:
			imported_num_hlayer_nodes = 0
		else:
			imported_num_hlayer_nodes = np.size(hlayers[0])
		imported_num_outputs = np.size(outputs)

		if override_structure:
			self.inputs, self.hlayers, self.outputs = inputs, hlayers, outputs
			self.num_inputs = imported_num_inputs
			self.num_hlayers = imported_num_hlayers
			self.num_hlayers_nodes = imported_num_hlayer_nodes
			self.num_outputs = imported_num_outputs

		else:
			if imported_num_inputs == self.num_inputs and imported_num_hlayers == self.num_hlayers and imported_num_hlayer_nodes == self.num_hlayers_nodes and imported_num_outputs == self.num_outputs:
				self.inputs = inputs
				self.hlayers = hlayers
				self.outputs = outputs


			else:
				print("Import error, imported network structure does not match current network structure")
				return None

		self.generate_layers()

		print("Import successful")


	def visualize(self, open_media_file=True):
		"""
		Visualizes the neural network and renders its video in media/videos/VisualizeNeuralNetwork.mp4

		Parameters
		----------
		open_media_file: bool, optional
			If True, the .mp4 video will open automatically after rendering (default is True)
		"""
		self.export_parameters(message=False)
		visualize_object = visualize.VisualizeNeuralNetwork()
		visualize_object.receive_inputs()
		os.remove("parameters.txt")
		visualize_object.play_render(open_media_file)


	def evaluate(self):
		# At this point, we have a layers list which we want to pass in for the helper functions
		# I want to call a single function here which will return a list of the evaluated outputs of the neural network
		return evaluation.evaluate_neural_network_outputs(self.layers, self.activation_function)

		



'''
Next steps:
- Implement loss function
- Back propagation
'''