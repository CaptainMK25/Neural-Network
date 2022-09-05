import numpy as np

class Neural_Network():
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

			self.hlayers = np.array(hlayers)

			
			outputs_node_vector = [0 for i in range(num_hlayer_nodes)]
			outputs = [outputs_node_vector for i in range(num_outputs)]
			self.outputs = np.array(outputs, ndmin=2)

		else:
			outputs_node_vector = [0 for i in range(num_inputs)]
			outputs = [outputs_node_vector for i in range(num_outputs)]
			self.outputs = np.array(outputs, ndmin=2)


	def get_inputs(self):
		return self.inputs

	def get_hlayers(self):
		if self.num_hlayers >= 1:
			for i in self.hlayers:
				print(self.hlayers.view())

		else:
			return None

	def get_outputs(self):
		return self.outputs




test = Neural_Network(5, 1, 3, 2)

print(test.get_inputs())
print(test.get_hlayers())
print(test.get_outputs())




'''
Each vector will represent one node, we combine all those vectors into one matrix to create a whole input / hidden layer in one variable

Each input will go into each hidden layer node, so each hidden layer node vector will have num_inputs + 1 (for the bias) as length, then duplicate that into the number of hidden layer nodes
'''