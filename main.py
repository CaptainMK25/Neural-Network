import numpy as np
from utils import *

class NeuralNetwork():
	def __init__(self, num_inputs = 1, num_outputs = 1, num_hlayers = 0, num_hlayer_nodes = 1):
		self.num_inputs = num_inputs
		self.num_hlayers = num_hlayers
		self.num_hlayers_nodes = num_hlayer_nodes
		self.num_outputs = num_outputs

		self.inputs = np.array([0 for i in range(num_inputs)], ndmin=1)


		if num_hlayers >= 1:
			hlayer1_node_vector = [0 for i in range(num_inputs + 1)]
			hlayer1 = [hlayer1_node_vector for i in range(num_hlayer_nodes)]
			hlayer1 = np.array(hlayer1, ndmin=2)

			hlayers_node_vector = [0 for i in range(num_hlayer_nodes + 1)]
			other_hlayers = [hlayers_node_vector for j in range(num_hlayer_nodes)]
			other_hlayers = np.array(other_hlayers, ndmin=2)

			hlayers = [hlayer1]
			for i in range(1, num_hlayers):
				hlayers.append(other_hlayers)


			self.hlayers = hlayers

			last_hlayer_node_length = len(self.hlayers[len(self.hlayers) - 1][0])

			outputs_node_vector = [0 for i in range(last_hlayer_node_length)]
			outputs = [outputs_node_vector for i in range(num_outputs)]
			self.outputs = np.array(outputs, ndmin=2)

		else:
			self.hlayers = []
			self.num_hlayers_nodes = 0
			outputs_node_vector = [0 for i in range(num_inputs)]
			outputs = [outputs_node_vector for i in range(num_outputs)]
			self.outputs = np.array(outputs, ndmin=2)


	def get_inputs(self):
		return self.inputs

	def get_hlayers(self):
		if self.num_hlayers >= 1:
			return self.hlayers

		else:
			return None

	def get_outputs(self):
		return self.outputs



	def export_parameters(self, name = "parameters"):
		file = open(name + ".txt", mode="w")

		file.write(exporting.create_paramters_string(self.inputs, self.outputs, self.hlayers))

		file.close()

		print("Export Successful")


	def import_parameters(self, name="parameters", override_structure = True):
		file = open(name + ".txt", mode="r")

		raw_parameters = file.readlines()

		organized_parameters = importing.read_parameters(raw_parameters)
		inputs = organized_parameters[0]
		hlayers = organized_parameters[1]
		outputs = organized_parameters[2]

		if override_structure:
			self.inputs = inputs
			self.hlayers = hlayers
			self.outputs = outputs

		else:
			imported_num_inputs = np.size(inputs)
			imported_num_hlayers = len(hlayers)
			imported_num_hlayer_nodes = 0
			imported_num_outputs = np.size(outputs)

			if imported_num_hlayers >= 1:
				imported_num_hlayer_nodes = np.size(hlayers[0])

			if imported_num_inputs == self.num_inputs and imported_num_hlayers == self.num_hlayers and imported_num_hlayer_nodes == self.num_hlayers_nodes and imported_num_outputs == self.num_outputs:
				self.inputs = inputs
				self.hlayers = hlayers
				self.outputs = outputs
				

			else:
				print("Import error, imported network structure does not match current network structure")

		print("Import Successful")


		



test = NeuralNetwork(5, 1, 2, 2)

test.import_parameters()

print(test.get_inputs())
print(test.get_hlayers())
print(test.get_outputs())




'''
Next step:
- Error checking the overriden structure import
- I'd like to visualize the network, maybe do that with tkinter or something, idk
- Get the network working together, inputs going in, weights playing their role, outputs going out
- Implement loss function
- Back propagation
'''