# Loan Approval Prediction with Logistic Regression — and the Neural Network Basics Behind It

*A week 2 walkthrough of cleaning a real loan dataset, training a classifier that comfortably beats a coin flip, and the perceptron math that explains why it works — plus where it leads once you stack more of it together.*

Every loan application eventually collapses into a single yes-or-no decision. That makes it a textbook binary classification problem, and it's exactly the kind of problem this week's session used to walk through the full supervised-learning pipeline: load messy real-world data, clean it, encode it, train a model, and score it honestly. The session also introduced the fundamentals of neural networks — and, as it turns out, the model trained in the notebook is only one small step away from being a neural network itself.

**In this post:**

- Cleaning and encoding the [Loan Prediction dataset](https://www.geeksforgeeks.org/machine-learning/one-hot-encoding-vs-label-encoding/) for a classifier
- Why scikit-learn's convergence warning showed up, and what it's actually telling you
- Reading a confusion matrix instead of trusting accuracy alone
- The perceptron: the single building block every neural network is made of
- How a logistic regression model *is* a one-neuron neural network
- Activation functions, forward passes, and backpropagation, in plain terms

## Cleaning the data before any model sees it

The notebook works with the classic [Loan Prediction dataset](https://www.geeksforgeeks.org/machine-learning/one-hot-encoding-vs-label-encoding/): applicant income, credit history, dependents, property area, and a `Loan_Status` column that's either `Y` or `N`. Real datasets almost never arrive complete, and this one doesn't either — a quick `isnull().sum()` turns up gaps in four columns:

```
Dependents            12
LoanAmount            21
Loan_Amount_Term      14
Credit_History        49
```

The fix follows a standard rule of thumb: fill numeric-ish continuous columns with the **mean**, and fill categorical or count-like columns with the **mode** (the most frequent value):

```python
data['LoanAmount'] = data['LoanAmount'].fillna(data['LoanAmount'].mean())
data['Loan_Amount_Term'] = data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].mode()[0])
data['Credit_History'] = data['Credit_History'].fillna(data['Credit_History'].mode()[0])
data['Dependents'] = data['Dependents'].fillna(data['Dependents'].mode()[0])
```

It's a reasonable default for a first pass, though it's worth knowing the tradeoff: mean/mode imputation quietly shrinks variance and can distort a column's true distribution, which is why more advanced pipelines reach for k-nearest-neighbor or iterative imputers once the "quick and clean" pass isn't good enough.

## Turning categories into numbers

Models don't understand `"Male"` or `"Urban"` — they need numbers. The notebook reaches for scikit-learn's `LabelEncoder` on every categorical column: `Gender`, `Married`, `Education`, `Self_Employed`, `Property_Area`, and the target `Loan_Status`.

```python
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
data['Gender'] = le.fit_transform(data['Gender'])
```

This works cleanly for binary columns like `Gender` (`Male`/`Female` → `1`/`0`) and for the target column, since a single 0/1 label is exactly what a classifier's target should look like. `LabelEncoder` is designed specifically for that — a single 1-D array of labels — which is why scikit-learn's own documentation scopes it to encoding **target values**, not general feature columns ([scikit-learn docs](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html)).

> **The thing worth watching here:** `Property_Area` has three unrelated categories — Urban, Rural, Semiurban — and `LabelEncoder` turns them into `2`, `0`, `1`. Nothing about those categories is ordered, but the numbers now imply "Semiurban > Rural," and a model that weighs features linearly (like logistic regression) can pick up on that fake ordering. For unordered, multi-category *feature* columns, the safer default is **one-hot encoding** (`OneHotEncoder` or `pd.get_dummies`), which creates a separate binary column per category so no false ranking sneaks in ([GeeksforGeeks: One-Hot vs Label Encoding](https://www.geeksforgeeks.org/machine-learning/one-hot-encoding-vs-label-encoding/)). `LabelEncoder` is the right tool for the target; for feature columns with more than two unordered categories, one-hot is the better fit.

## What the target column actually looks like

Before training anything, the notebook plots `Loan_Status` as a bar chart and a pie chart. That step matters more than it looks: classification accuracy only means something in the context of how balanced the classes are. If 90% of applicants were approved, a model that approves everyone would already be "90% accurate" without learning a thing.

*(a bar and pie chart of approved-vs-rejected counts would go here — the notebook renders both, showing that approvals substantially outnumber rejections)*

## Training the classifier

With every column numeric, the target (`Loan_Status`) is separated from the features, and the data is split 85/15 into train and test sets:

```python
X = data.drop(['Loan_ID', 'Loan_Status'], axis=1)
Y = data['Loan_Status']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=2)

model = LogisticRegression()
model.fit(X_train, Y_train)
```

Running this throws a warning that's easy to dismiss as noise, but it isn't:

```
ConvergenceWarning: lbfgs failed to converge (status=1):
STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT.
```

`LogisticRegression`'s default solver, `lbfgs`, defaults to 100 iterations, and with unscaled income columns running into the thousands sitting next to 0/1 encoded flags, the optimizer simply needs more steps (or better-scaled input) to settle on its final weights ([Forecastegy: fixing logistic regression convergence](https://forecastegy.com/posts/how-to-solve-logistic-regression-not-converging-in-scikit-learn/)). The two standard fixes are to raise `max_iter` (e.g. `LogisticRegression(max_iter=1000)`) or, the more durable fix, to scale the features first with `StandardScaler` in a pipeline — scaling reshapes the optimization landscape so `lbfgs` converges in far fewer steps. The model still fit and produced usable results here, but the warning is scikit-learn correctly flagging that the reported coefficients aren't fully settled.

## Scoring it honestly

The model landed at:

```
Model Accuracy: 77.78%
Confusion Matrix:
[[16 15]
 [ 5 54]]
```

That confusion matrix is more informative than the single accuracy number sitting above it. Reading it against the label order (`0 = N`, `1 = Y`): the test set held 31 applicants who were actually rejected and 59 who were actually approved. The model correctly caught 16 of the 31 true rejections and 54 of the 59 true approvals.

> **Where accuracy hides the real story:** 59 of the 90 test applicants (about two-thirds) were genuinely approved, so a model that blindly approved *everyone* would already score around 66% accuracy while learning nothing. 77.78% beats that lazy baseline, but the matrix shows the model still approved 15 of the 31 applicants who should have been rejected — a false-approval rate lenders care about a lot more than the headline accuracy number suggests.

This is exactly why the confusion matrix — and metrics like precision and recall pulled from it — matter alongside accuracy, especially on any dataset where the classes aren't evenly split.

## From logistic regression to neural networks

Here's the connective thread the session drew out: logistic regression isn't a separate technique from neural networks — it's the smallest possible one. A logistic regression model takes every feature, multiplies each by a learned weight, adds a bias term, sums it all up, and squashes the result through a **sigmoid function** into a probability between 0 and 1. That is, feature-for-feature, exactly what a single artificial neuron does.

### The perceptron: one neuron, four parts

The perceptron — the original, simplest artificial neuron — has four ingredients ([GeeksforGeeks: What is Perceptron](https://www.geeksforgeeks.org/deep-learning/what-is-perceptron-the-simplest-artificial-neural-network/)):

1. **Inputs** — the feature values (income, credit history, dependents, and so on).
2. **Weights** — one learned number per input, controlling how much that input should influence the outcome.
3. **Bias** — a constant added to the weighted sum, letting the neuron shift its decision boundary independent of the inputs.
4. **Activation function** — a non-linear function applied to the weighted sum to produce the neuron's actual output.

A neural network is just many of these neurons arranged in layers, each layer's output feeding the next layer's input — commonly called a **multilayer perceptron (MLP)**. The single logistic regression model trained above is, structurally, a network with exactly one neuron and one layer.

### Activation functions: why they matter and which one to use where

Without an activation function, stacking layers would be pointless — a chain of purely linear operations collapses back into one linear operation, no matter how many layers you add. The activation function is what lets a network learn curved, non-linear decision boundaries instead of only straight lines.

| Function | Typical use | Output range |
|---|---|---|
| **Sigmoid** | Binary classification output layer (this is what logistic regression uses) | 0 to 1 |
| **Softmax** | Multi-class classification output layer (one score per class, all summing to 1) | 0 to 1 (as a set) |
| **ReLU** | Default choice for hidden layers | 0 to ∞ |
| **Tanh** | Hidden layers, when zero-centered output helps training | −1 to 1 |

The current, well-established default is: use **ReLU** in hidden layers because it keeps gradients from shrinking to nothing in deep networks (a failure mode sigmoid is prone to), and pick the output activation based on the task — **sigmoid** for a single yes/no output, **softmax** when choosing among several mutually exclusive classes ([GeeksforGeeks: Activation Functions in Neural Networks](https://www.geeksforgeeks.org/machine-learning/activation-functions-neural-networks/); [Towards Data Science: choosing the right activation function](https://towardsdatascience.com/how-to-choose-the-right-activation-function-for-neural-networks-3941ff0e6f9c/)). Notice the loan model's output layer — sigmoid, for a yes/no decision — already follows that same rule; it just never had a hidden layer to apply ReLU to.

### How a network actually learns

Training a neural network (or, for that matter, the logistic regression model above) repeats the same loop:

1. **Forward pass** — push the inputs through the weights, biases, and activation functions to get a prediction.
2. **Loss calculation** — measure how wrong that prediction was against the true label.
3. **Backpropagation** — work backward through the network, using the chain rule to figure out exactly how much each individual weight contributed to that error ([IBM: What is Backpropagation](https://www.ibm.com/think/topics/backpropagation)).
4. **Gradient descent update** — nudge every weight slightly in the direction that reduces the error, scaled by a **learning rate**: too large and training overshoots and destabilizes; too small and it crawls toward a solution ([IBM: What is Learning Rate](https://www.ibm.com/think/topics/learning-rate); [MachineLearningMastery: configuring the learning rate](https://machinelearningmastery.com/learning-rate-for-deep-learning-neural-networks/)).

One full pass through the entire training set is an **epoch**; real training runs repeat this loop for many epochs until the loss stops meaningfully improving. `model.fit(X_train, Y_train)` in the notebook is doing a compressed version of exactly this loop — scikit-learn's `lbfgs` solver is just a more efficient optimizer than plain gradient descent, iterating on the same one-neuron weights until the convergence criteria are met (which, per that warning above, it didn't quite finish doing within the default iteration budget).

## Key takeaways

- Handle missing values deliberately: mean for continuous columns, mode for categorical/count columns — and know it's a quick fix, not a permanent one.
- `LabelEncoder` is built for target columns; unordered multi-category *feature* columns are safer one-hot encoded to avoid implying a false ranking.
- A `ConvergenceWarning` on `LogisticRegression` is a real signal — raise `max_iter` or scale features with `StandardScaler` rather than ignoring it.
- Always read the confusion matrix next to accuracy — a high accuracy score can still hide a lopsided error pattern that matters for the actual decision being made.
- Logistic regression and a single artificial neuron are the same computation: weighted sum, plus bias, through a sigmoid. Neural networks are what happens when you stack many of these into layers.
- ReLU is the default for hidden layers; sigmoid or softmax belong on the output layer depending on whether the task is binary or multi-class.
- Every network — from one neuron to a hundred layers — learns the same way: forward pass, measure loss, backpropagate the error, and nudge weights via gradient descent at a chosen learning rate, over and over across epochs.

## Further reading / sources

- [scikit-learn: `LabelEncoder` documentation](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html)
- [GeeksforGeeks: One Hot Encoding vs Label Encoding](https://www.geeksforgeeks.org/machine-learning/one-hot-encoding-vs-label-encoding/)
- [Forecastegy: How to Solve Logistic Regression Not Converging in Scikit-Learn](https://forecastegy.com/posts/how-to-solve-logistic-regression-not-converging-in-scikit-learn/)
- [scikit-learn: Release History](https://scikit-learn.org/stable/whats_new.html)
- [GeeksforGeeks: What is Perceptron — the Simplest Artificial Neural Network](https://www.geeksforgeeks.org/deep-learning/what-is-perceptron-the-simplest-artificial-neural-network/)
- [IBM: What is Backpropagation?](https://www.ibm.com/think/topics/backpropagation)
- [GeeksforGeeks: Activation Functions in Neural Networks](https://www.geeksforgeeks.org/machine-learning/activation-functions-neural-networks/)
- [Towards Data Science: How to Choose the Right Activation Function for Neural Networks](https://towardsdatascience.com/how-to-choose-the-right-activation-function-for-neural-networks-3941ff0e6f9c/)
- [IBM: What is Learning Rate?](https://www.ibm.com/think/topics/learning-rate)
- [MachineLearningMastery: How to Configure the Learning Rate When Training Deep Learning Neural Networks](https://machinelearningmastery.com/learning-rate-for-deep-learning-neural-networks/)
