# This is a neural net class. This takes inputs of the size of the neural net and generates random weights and biases. These neural nets can
# make children by randomly selecting between weights and biases of two parents. The resulting child is then randomly mutated slightly
#
# Jacob Karty 12/3/2024

import numpy as np

class NeuralNetwork:
    """Initialize the neural net. The input is an array of integers. Each integer represents the number of nodes in that layer."""
    def __init__(self, inputs):
        self.inputs = inputs
        self.weights = []
        self.biases = []
        for i in range(len(inputs)-1):
            weight = np.random.rand(inputs[i], inputs[i+1]) * 2 - 1
            self.weights.append(weight)
            bias = np.random.rand(1, inputs[i+1]) * 2 - 1
            self.biases.append(bias)


    """calculates through the neural network. Uses the hyperbolic tangent as the activation function for all the layers
    except for the last layer, where a sign activation function is used, as buttons are either pressed or not pressed."""
    def calculate_forward(self, value):
        for i in range(len(self.weights)):
            value = np.tanh(np.dot(value, self.weights[i])) + self.biases[i]
        return np.where(value >=0, 1, -1)[0]
    
    """Prints the neural network (instead of creating saves and loads)"""
    def print_network(self):
        print("__________________________________________________________________")
        print("Weights:")
        for weight in self.weights:
            self.print_array(weight)
        print("Biases:")
        for bias in self.biases:
            self.print_array(bias)
        print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    
    """Helper function for print_network. Prints a 2D array with comma seperated values so that they can be copied and pasted into the checkpoint code"""
    def print_array(self, array):
        out = ""
        out += "["
        for arr in array:
            out += "["
            for value in arr:
                out += str(value)
                out += ", "
            out = out[:-2]
            out += "], "
        out = out[:-2]
        out += "]"
        print(out)
    
    """Create a child with another neural network by using a genetic algorithm with the weights and biases of the
    neural network"""
    def make_child(self, other, mutation_rate=0.1):
        child = NeuralNetwork(self.inputs)
        child.weights = []
        child.biases = []
        for i in range(len(self.inputs)-1):
            child_weight = self.random_mix(self.weights[i], other.weights[i])
            child_weight = self.mutate_child(child_weight, mutation_rate)
            child.weights.append(child_weight)
            child_bias = self.random_mix(self.biases[i], other.biases[i])
            child_bias = self.mutate_child(child_bias, mutation_rate)
            child.biases.append(child_bias)
        return child

    """Helper function to cross over the two parents"""
    def random_mix(self, X, Y):
        choice = np.random.randint(2, size = X.size).reshape(X.shape).astype(bool)
        return np.where(choice, X, Y)
    
    """Helper function to indroduce randomness to the system through mutation"""
    def mutate_child(self, matrix, mutation_rate):
        mask = np.random.rand(matrix.size).reshape(matrix.shape)
        return np.where(mask>mutation_rate, matrix, matrix + np.random.rand()*mutation_rate - mutation_rate/2)
    
    """Generates a 2D matrix where the each value represents the number of children agents i and j create. inputs
    are the number of parent agents and the number of children desired"""
    def generate_weighted_reproduction_matrix(num_parents, num_children):
        # Calculate weights for each pair (i, j)
        pairs = [(i, j) for i in range(num_parents) for j in range(i + 1, num_parents)]
        weights = np.array([(num_parents - i) + (num_parents - j) for i, j in pairs])
        total_weight = weights.sum()
        
        # Allocate children proportionally
        allocated_children = (weights * num_children) // (total_weight)
        out = np.zeros((num_parents, num_parents), dtype=int)
        for idx, (i, j) in enumerate(pairs):
            out[i, j] = allocated_children[idx]
        
        # Account for rounding errors by distribuitng remaining children to ramaining heavily weighted pairs
        total_allocated = allocated_children.sum()
        remaining_children = num_children - total_allocated
        sorted_indices = np.argsort(-weights)
        for idx in sorted_indices:
            if remaining_children <= 0:
                break
            i, j = pairs[idx]
            out[i, j] += 1
            remaining_children -= 1
        
        return out

# test the neural network
if __name__ == '__main__':
    test1 = NeuralNetwork([2, 3])
    test1.print_network()

    test2 = NeuralNetwork([2, 3])
    test2.print_network()

    child = test1.make_child(test2, 0.1)
    child.print_network()

    print(child.calculate_forward([1, 2]))