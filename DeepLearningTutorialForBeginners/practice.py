import numpy as np

# 示例数据 (请替换为您的数据集)
x = np.random.rand(4096, 10)  # 4096 个样本，10 个特征
y = np.random.randint(0, 2, 4096)  # 确保 y 也有 4096 个样本

# 检查维度
print("x shape:", x.shape)
print("y shape:", y.shape)

# 进行逻辑回归
from sklearn import linear_model
from sklearn.model_selection import train_test_split

# 数据切分
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# 初始化逻辑回归模型
logreg = linear_model.LogisticRegression(random_state=42, max_iter=150)

# 拟合模型
logreg.fit(x_train, y_train)

# 计算准确率
train_acc = logreg.score(x_train, y_train)
test_acc = logreg.score(x_test, y_test)

# 打印准确率
print("train accuracy: {:.4f}".format(train_acc))
print("test accuracy: {:.4f}".format(test_acc))


def initialize_parameters_and_layer_sizes_NN(x_train, y_train):
    parameters = {"weight1": np.random.randn(3, x_train.shape[0]) * 0.1,
                  "bias1": np.zeros((3, 1)),
                  "weight2": np.random.randn(y_train.shape[0], 3) * 0.1,
                  "bias2": np.zeros((y_train.shape[0], 1))}

    return parameters


def forward_propagation_NN(x_train, parameters):
    Z1 = np.dot(parameters["weight1"], x_train) + parameters["bias1"]
    A1 = np.tanh(Z1)
    Z2 = np.dot(parameters["weight2"], A1) + parameters["bias2"]
    A2 = sigmoid(Z2)

    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}

    return A2, cache

def compute_cost_NN(A2, Y, parameters):
    logprobs = np.multiply(np.log(A2), Y)
    cost = -np.sum(logprobs) / Y.shape[1]
    return cost


def backward_propagation_NN(parameters, cache, X, Y):
    dZ2 = cache["A2"] - Y
    dw2 = np.dot(dZ2, cache["A1"].T) / X.shape[1]
    db2 = np.sum(dZ2, axis=1, keepdims=True) / X.shape[1]

    dZ1 = np.dot(parameters["weight2"].T, dZ2) * (1 - np.power(cachee["A1"], 2))
    dw1 = np.dott(dZ1, X.T) / X.shape[1]
    db1 = np.sum(dZ1, axis=1, keepdims=True) / X.shape[1]

    grads = {"dweight1": dw1,
             "dbias1": db1,
             "dweight2": dw2,
             "dbias2": db2}

    return grads


def update_parameters_NN(parameters, grads, learning_rate=0.01):
    parameters = {"weight1": parameters["weight1"] - learning_rate * grads["dweight1"], \
                  "bias1": parameters["bias1"] - learning_rate * grads["dbias1"],
                  "weight2": parameters["weight2"] - learning_rate * grads["dweight2"],
                  "bias2": parameters["bias2"] - learning_rate * grads["dbias2"]}

    return parameters


def predict_NN(parameters, x_test):
    A2, cache = forward_propagation_NN(x_test, parameters)
    Y_prediction = np.zeros((1, x_test.shape[1]))

    for i in range(A2.shape[1]):
        if A2[0, i] <= 0.5:
            Y_prediction[0, i] = 0
        else:
            Y_prediction[0, i] = 1

    return Y_prediction


def two_layer_neural_network(x_train, y_train, x_test, y_test, num_iterations):
    cost_list = []
    index_list = []

    parameters = initialize_parameters_and_layer_sizes_NN(x_train, y_train)

    for i in range(0, num_iterations):

        A2, cache = forward_propagation_NN(x_train, parameters)

        cost = compute_cost_NN(A2, y_train, parameters)
        # A2, y_train, parameters
        grads = backward_propagation_NN(parameters, cache, x_train, y_train)

        parameters = update_parameters_NN(parameters, grads)

        if i % 100 == 0:
            cost_list.append(cost)
            index_list.append(i)
            print("Cost after iteration %i: %f" % (i, cost))

        plt.plot(index_list, cost_list)
        plt.xlabel(index_list, rotation='vertical')
        plt.xlabel("Number of Iterarion")
        plt.ylabel("Cost")
        plt.show()

        # predict
    y_prediction_test = predict_NN(parameters, x_test)
    y_prediction_train = predict_NN(parameters, x_train)

    # Print train/test Errors
    print("train accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_train - y_train)) * 100))
    print("test accuracy: {} %".format(100 - np.mean(np.abs(y_prediction_test - y_test)) * 100))
    return parameters

def sigmoid(z):
    y_head = 1/(1+np.exp(-z))
    return y_head

parameters = two_layer_neural_network(x_train, y_train, x_test, y_test, num_iterations=2500)
