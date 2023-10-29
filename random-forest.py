import numpy as np
from collections import Counter
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd


#cria um novo nó
class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None,*,value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        
    def is_leaf_node(self):
        return self.value is not None


class DecisionTree:
    #inicializa os hiperparâmetros da árvore de decisão, como a profundidade máxima da árvore e o número mínimo de amostras para divisão.
    def __init__(self, min_samples_split=2, max_depth=100, n_features=None):
        self.min_samples_split=min_samples_split
        self.max_depth=max_depth
        self.n_features=n_features
        self.root=None
    #Este método é usado para treinar a árvore de decisão com os dados de treinamento.
    def fit(self, X, y):
        self.n_features = X.shape[1] if not self.n_features else min(X.shape[1],self.n_features)
        self.root = self._grow_tree(X, y)
    #Este método é uma função interna que cria a árvore de decisão de forma recursiva. Ele verifica os critérios de parada, encontra a melhor divisão e cria nós filhos.
    def _grow_tree(self, X, y, depth=0):
        n_samples, n_feats = X.shape
        n_labels = len(np.unique(y))

        # check the stopping criteria
        if (depth>=self.max_depth or n_labels==1 or n_samples<self.min_samples_split):
            leaf_value = self._most_common_label(y)
            return Node(value=leaf_value)

        feat_idxs = np.random.choice(n_feats, self.n_features, replace=False)

        # find the best split
        best_feature, best_thresh = self._best_split(X, y, feat_idxs)

        # create child nodes
        left_idxs, right_idxs = self._split(X[:, best_feature], best_thresh)
        left = self._grow_tree(X[left_idxs, :], y[left_idxs], depth+1)
        right = self._grow_tree(X[right_idxs, :], y[right_idxs], depth+1)
        return Node(best_feature, best_thresh, left, right)

    #Encontra a melhor divisão possível em uma característica.
    def _best_split(self, X, y, feat_idxs):
        best_gain = -1
        split_idx, split_threshold = None, None

        for feat_idx in feat_idxs:
            X_column = X[:, feat_idx]
            thresholds = np.unique(X_column)

            for thr in thresholds:
                # calculate the information gain
                gain = self._information_gain(y, X_column, thr)

                if gain > best_gain:
                    best_gain = gain
                    split_idx = feat_idx
                    split_threshold = thr

        return split_idx, split_threshold

    #Calcula o ganho de informação para uma possível divisão.
    def _information_gain(self, y, X_column, threshold):
        # parent entropy
        parent_entropy = self._entropy(y)

        # create children
        left_idxs, right_idxs = self._split(X_column, threshold)

        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0
        
        # calculate the weighted avg. entropy of children
        n = len(y)
        n_l, n_r = len(left_idxs), len(right_idxs)
        e_l, e_r = self._entropy(y[left_idxs]), self._entropy(y[right_idxs])
        child_entropy = (n_l/n) * e_l + (n_r/n) * e_r

        # calculate the IG
        information_gain = parent_entropy - child_entropy
        return information_gain
    #Divide os índices das amostras com base em um valor de corte.
    def _split(self, X_column, split_thresh):
        left_idxs = np.argwhere(X_column <= split_thresh).flatten()
        right_idxs = np.argwhere(X_column > split_thresh).flatten()
        return left_idxs, right_idxs
    #Calcula a entropia de um conjunto de dados.
    def _entropy(self, y):
        hist = np.bincount(y)
        ps = hist / len(y)
        return -np.sum([p * np.log(p) for p in ps if p>0])

    #Retorna a classe mais comum em um conjunto de dados.
    def _most_common_label(self, y):
        counter = Counter(y)
        value = counter.most_common(1)[0][0]
        return value
    #Faz previsões usando a árvore de decisão treinada.
    def predict(self, X):
        return np.array([self._traverse_tree(x, self.root) for x in X])
    #Função interna para percorrer a árvore durante a previsão.
    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
        
    #A classe RandomForest representa um conjunto de árvores de decisão combinadas em uma floresta aleatória.
class RandomForest:
    #O construtor da classe RandomForest inicializa os hiperparâmetros da floresta aleatória, como o número de árvores, 
    # profundidade máxima, número mínimo de amostras para divisão e o número de características usadas em cada árvore.
    def __init__(self, n_trees=10, max_depth=10, min_samples_split=2, n_feature=None):
        self.n_trees = n_trees
        self.max_depth=max_depth
        self.min_samples_split=min_samples_split
        self.n_features=n_feature
        self.trees = []
    #Este método treina a floresta aleatória com os dados de treinamento, criando várias árvores de decisão.
    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees): #cria arvores
            tree = DecisionTree(max_depth=self.max_depth,
                            min_samples_split=self.min_samples_split,
                            n_features=self.n_features)
            X_sample, y_sample = self._bootstrap_samples(X, y)
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)
    #Seleciona amostras aleatórias com substituição para treinar cada árvore.
    def _bootstrap_samples(self, X, y):
        n_samples = X.shape[0]
        #print(n_samples)
        idxs = np.random.choice(n_samples, n_samples, replace=True)
        return X[idxs], y[idxs]
    #Retorna a classe mais comum em um conjunto de dados.
    def _most_common_label(self, y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common
    #Faz previsões usando as árvores na floresta e retorna a classe mais comum como resultado.
    def predict(self, X):
        predictions = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(predictions, 0, 1)
        predictions = np.array([self._most_common_label(pred) for pred in tree_preds])
        return predictions



arq1 = 'treino_sinais_vitais_com_label.csv'

col_names = ['pSist','pDiast','qPA', 'pulso', 'resp', 'gravid', 'classe']
data = pd.read_csv(arq1, skiprows=1, header=None, names=col_names)
print(data.head())
print(data.head())

X = data.iloc[:, :-1].values
Y = data.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)#, random_state=1234
clf = RandomForest(n_trees=10, max_depth=10, min_samples_split=2)
clf.fit(X_train, y_train)
predictions = clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, predictions)}')