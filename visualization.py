from manim import *
import numpy as np

class VisualizeNeuralNetwork(Scene):
    def construct(self):
        dot1 = Dot(np.array([3, 3, 0]), color=WHITE, radius=0.1)
        circle_1 = Circle().move_to(dot1)
        circle_2 = Circle(radius=1.5, color=GREEN)

        self.play(Create(dot1))
        self.play(Create(circle_1))
        self.play(Create(circle_2))

        self.wait(100)

        


'''
In a frame with w width, l length and where x represents the location of a node on the frame horizontally and y represents the location of a node on the frame vertically

We need the number of layers, including input and output, and we need to setup a certain distance between each layer of nodes, say 150 pixels, as well a certain distance between each node in the layer, say 50 pixels

So dh = 150, dv = 50


In the simplest network of 1 input and 1 output:
Input node: Location is ((w-150)/2, )
Output node: Location is ((w+150)/2, )

'''