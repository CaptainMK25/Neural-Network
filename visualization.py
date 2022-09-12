from manim import *
import numpy as np

class VisualizeNeuralNetwork(Scene):
    def construct(self):
        dot1 = Dot(np.array([0, 4, 1]), color=WHITE, radius=0.1)
        circle_1 = Circle().move_to(dot1)
        circle_2 = Circle(radius=1.5, color=GREEN)

        self.play(Create(dot1))
        self.play(Create(circle_1))
        self.play(Create(circle_2))

        self.wait(100)


'''
np.array([x,y,z]):
x: controls the x-axis position, interval [-7, 7]
y: controls the y-axs position, interval [-4, 4]
z: N/A
'''


'''
To visualize a neural network, we'll need to define some constants before getting each node's coordinates:
- Length between 2 consecutive layers: dh = 1
- Length between 2 consecutive nodes in a single layer: dv = 0.5
- Radius of any node: radius = 0.5

Side note: We'll have to develop functions to get these constant values before rendering the visualization to avoid the network not fitting the frame


With a function that takes in a list of layers (3d list, list of lists of lists), we can define the following:
- num_layers = len(list of layers)
- middle_layer_index = (num_layers - 1) / 2
- current_layer_index = i from the layers_list for loop
- middle_node_index = (len(current_layer) - 1) / 2
- current_node_index = j from the current_layer for loop


To get the x_value coordinate of each node, we use the following logic:
difference_index = middle_index - current_index

For every 1 in the difference index, we add dh + 2*radius to the total

For every 0.5 (after the 1), we add dh/2 + radius


To get the y_value of each node, we use the following logic:
difference_index = middle_index - current_index

For every 1 in the difference index, we add dv + 2*radius to the total

For every 0.5 (after the 1), we add dv/2 + radius

'''