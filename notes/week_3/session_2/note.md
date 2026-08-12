# Neural Network

## Types of NN

Neural networks come in different architectures, each optimized for specific data types and tasks. The main categories differ in how they process input, layer structure, and the patterns they excel at capturing.

### Key Points

- **ANN (Artificial Neural Networks)**: Works best with structured/tabular data; uses fully connected layers
- **CNN (Convolutional Neural Networks)**: Specialized for images and videos; uses convolutional filters to detect spatial patterns
- **RNN (Recurrent Neural Networks)**: Designed for sequential/unstructured data like text, speech, and time series; maintains hidden state to capture temporal dependencies
- **Transformers**: Modern architecture based on attention mechanisms; processes data in parallel and excels at sequence-to-sequence tasks, now state-of-the-art for NLP

### Examples

**ANN**: Predicting house prices from features like square footage, bedrooms, location. Each input feature is fully connected to hidden layers.

**CNN**: Image classification (cats vs. dogs), object detection in photos. Convolutional filters slide across the image to detect edges, textures, and objects at different scales.

**RNN**: Machine translation (English to French), sentiment analysis of text reviews, time series forecasting. Processes text word-by-word or time series point-by-point, maintaining memory of previous inputs.

**Transformers**: Large Language Models like GPT, BERT; machine translation with attention. Processes entire sequences simultaneously using self-attention mechanisms to weight the importance of each token relative to others, enabling parallel processing and capturing long-range dependencies better than RNNs.

## Activation Function

- Captures non-linear patterns from the data
- Mathematical function applied to neuron outputs
- Used in hidden layers and output layers
- Allows neural networks to learn complex decision boundaries

### Types of Activation Functions

1. **Sigmoid**
2. **TanH (Hyperbolic Tangent)**
3. **Softmax**
4. **ReLU (Rectified Linear Unit)**

---

### 1. Sigmoid

**Explanation:**
The sigmoid function is a smooth, nonlinear activation function expressed as σ(x) = 1/(1+e^(-x)). It transforms any input value into an output between 0 and 1. The function has an "S" shape, starting with slow increase, rapidly approaching 1, and then leveling off.

**Key Characteristics:**
- Maps input values to range between 0 and 1
- Smooth and continuous function
- Zero-centered output: No (outputs range from 0-1)
- Primary use: Binary classification problems
- Used in output layer for binary classification

**Output Value Range:** (0, 1) — strictly between 0 and 1

**Advantages:**
- Intuitive probability interpretation
- Smooth gradient for backpropagation
- Well-established in logistic regression

**Limitations:**
- Suffers from "vanishing gradient problem" during backpropagation
- Slower convergence compared to other modern activation functions
- Not zero-centered, which can slow down learning

---

### 2. TanH (Hyperbolic Tangent)

**Explanation:**
TanH is a shifted version of the sigmoid function that outputs values ranging from -1 to +1. It is mathematically expressed as tanh(x) = (e^x - e^(-x)) / (e^x + e^(-x)). It provides zero-centered outputs, making it more effective for gradient-based learning.

**Key Characteristics:**
- Maps input values to range between -1 and +1
- Zero-centered output: Yes (outputs are symmetric around 0)
- Smoother gradient than sigmoid
- Preferred for hidden layers due to zero-centered output
- Faster convergence than sigmoid

**Output Value Range:** (-1, +1) — between -1 and 1

**Advantages:**
- Zero-centered output facilitates easier learning for subsequent layers
- Stronger gradients (derivative is steeper)
- Faster convergence than sigmoid
- Better for hidden layer activations

**Limitations:**
- Still susceptible to vanishing gradient problem (though less severe than sigmoid)
- More computationally expensive than ReLU
- Not ideal for very deep networks

---

### 3. Softmax

**Explanation:**
Softmax is a normalized exponential function that converts a vector of numbers into a probability distribution. It outputs values that sum to 1, making it ideal for multi-class classification problems. The function treats all outputs as class probabilities.

**Key Characteristics:**
- Normalizes outputs to probabilities
- Outputs for each class are between 0 and 1
- Sum of all outputs equals 1
- Provides probability interpretation for classification
- Primarily used in output layer for multi-class problems

**Output Value Range:** (0, 1) for each class; all outputs sum to 1

**Advantages:**
- Perfect for multi-class classification
- Probabilistic interpretation of outputs
- Differentiable for backpropagation
- Clear probability distribution across classes

**Limitations:**
- Only used in output layer, not hidden layers
- Computationally more expensive than ReLU
- Sensitive to large input values (numerical stability considerations)

**Formula:** For output unit i: softmax(z_i) = e^(z_i) / Σ(e^(z_j)) for all j

---

### 4. ReLU (Rectified Linear Unit)

**Explanation:**
ReLU is a modern activation function that replaces all negative input values with 0 and keeps positive values unchanged. Expressed as f(x) = max(0, x), it is computationally simple and highly efficient. ReLU and its variants are the most widely used activation functions in deep learning today.

**Key Characteristics:**
- Maps negative values to 0
- Keeps positive values unchanged
- Extremely computationally efficient
- Non-smooth at zero (not differentiable at x=0, but differentiable elsewhere)
- Preferred for hidden layers in deep networks

**Output Value Range:** [0, ∞) — zero to infinity

**Advantages:**
- Computationally efficient (simple max operation)
- Avoids vanishing gradient problem
- Faster training convergence
- Works exceptionally well for deep neural networks
- Reduces computational burden significantly

**Limitations:**
- "Dying ReLU Problem" — neurons can become inactive and stop learning
- Output is not zero-centered
- Not differentiable at x=0 (though practically not an issue)
- Can produce unbounded outputs for large positive values

**Variants:**
- **Leaky ReLU:** f(x) = x if x > 0, else αx (where α is a small positive constant like 0.01)
- **ELU (Exponential Linear Unit):** Similar to Leaky ReLU but with exponential form for negative values

---

### Summary Comparison Table

| Function | Range | Zero-Centered | Use Case | Best For |
|----------|-------|---------------|----------|----------|
| Sigmoid | (0, 1) | No | Binary classification | Output layer (binary) |
| TanH | (-1, +1) | Yes | Hidden layers, binary | Hidden layers |
| Softmax | (0, 1) sum=1 | No | Multi-class prob. | Output layer (multi-class) |
| ReLU | [0, ∞) | No | Hidden layers, deep nets | Hidden layers (modern) |

---

## Optimizers

- gradient decent

- adam
- adaGrad
- RMSProp

## References

- [Neural networks: Activation functions - Google Developers](https://developers.google.com/machine-learning/crash-course/neural-networks/activation-functions)
- [Sigmoid Function - MachineLearningMastery.com](https://machinelearningmastery.com/a-gentle-introduction-to-sigmoid-function/)
- [Activation Functions in Neural Networks - GeeksforGeeks](https://www.geeksforgeeks.org/machine-learning/activation-functions-neural-networks/)
- [Activation Functions 101 - LinkedIn](https://www.linkedin.com/pulse/activation-functions-101-sigmoid-tanh-relu-softmax-ben-hammouda)
