import math
import random

random.seed(42)

def random_matrix(rows, cols):
    return [[random.uniform(-1, 1) for _ in range(cols)] for _ in range(rows)]

def zeros(rows, cols):
    return [[0.0 for _ in range(cols)] for _ in range(rows)]

def dot(A, B):
    m = len(A)
    n = len(A[0])
    p = len(B[0])
    C = zeros(m, p)
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def transpose(A):
    m = len(A)
    n = len(A[0])
    return [[A[i][j] for i in range(m)] for j in range(n)]

def add(A, B):
    return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def subtract(A, B):
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def multiply(A, B):
    return [[A[i][j] * B[i][j] for j in range(len(A[0]))] for i in range(len(A))]

def apply(A, func):
    return [[func(A[i][j]) for j in range(len(A[0]))] for i in range(len(A))]

def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_deriv(x):
    return x * (1.0 - x)

class MLP:
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = random_matrix(input_size, hidden_size)
        self.b1 = zeros(1, hidden_size)
        self.W2 = random_matrix(hidden_size, output_size)
        self.b2 = zeros(1, output_size)

    def forward(self, X):
        self.X = X
        
        b1_broadcast = [[self.b1[0][j] for j in range(len(self.b1[0]))] for _ in range(len(X))]
        self.Z1 = add(dot(X, self.W1), b1_broadcast)
        self.A1 = apply(self.Z1, sigmoid)
        
        b2_broadcast = [[self.b2[0][j] for j in range(len(self.b2[0]))] for _ in range(len(self.A1))]
        self.Z2 = add(dot(self.A1, self.W2), b2_broadcast)
        self.A2 = apply(self.Z2, sigmoid)
        
        return self.A2

    def backward(self, Y, learning_rate):
        m = len(self.X)
        
        error = subtract(self.A2, Y)
        sig_deriv_A2 = apply(self.A2, sigmoid_deriv)
        dZ2 = multiply(error, sig_deriv_A2)
        
        dW2 = dot(transpose(self.A1), dZ2)
        db2 = [[sum(dZ2[i][j] for i in range(m)) for j in range(len(dZ2[0]))]]
        
        dA1 = dot(dZ2, transpose(self.W2))
        sig_deriv_A1 = apply(self.A1, sigmoid_deriv)
        dZ1 = multiply(dA1, sig_deriv_A1)
        
        dW1 = dot(transpose(self.X), dZ1)
        db1 = [[sum(dZ1[i][j] for i in range(m)) for j in range(len(dZ1[0]))]]
        
        self.W2 = subtract(self.W2, apply(dW2, lambda x: x * learning_rate))
        self.b2 = subtract(self.b2, apply(db2, lambda x: x * learning_rate))
        self.W1 = subtract(self.W1, apply(dW1, lambda x: x * learning_rate))
        self.b1 = subtract(self.b1, apply(db1, lambda x: x * learning_rate))

if __name__ == "__main__":
    X = [[0, 0], [0, 1], [1, 0], [1, 1]]
    Y = [[0], [1], [1], [0]]

    mlp = MLP(input_size=2, hidden_size=4, output_size=1)
    
    epochs = 15000
    learning_rate = 1.0

    for epoch in range(epochs):
        mlp.forward(X)
        mlp.backward(Y, learning_rate)

    predictions = mlp.forward(X)
    print("XOR Problem Predictions after training:")
    for i in range(len(X)):
        pred_val = predictions[i][0]
        expected = Y[i][0]
        print(f"Input: {X[i]} -> Prediction: {pred_val:.4f} | Expected: {expected}")