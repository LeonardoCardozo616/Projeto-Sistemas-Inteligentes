import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        # Nó de decisão
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain
        
        # Nó folha
        self.value = value


class DecisionTreeClassifier():
    def __init__(self, min_samples_split=2, max_depth=2):
        # raiz da árvore 
        self.root = None
        
        # limites
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        
    ''' Função recursiva que cria a árvore ''' 
    def build_tree(self, dataset, curr_depth=0):
        X, Y = dataset[:,:-1], dataset[:,-1]
        num_samples, num_features = np.shape(X)
        
        # Separa até que as condições de parada sejam encontradas
        if num_samples>=self.min_samples_split and curr_depth<=self.max_depth:
            # encontra a melhor divisão
            best_split = self.get_best_split(dataset, num_samples, num_features)
            # verifica se o ganho de informação é positivo
            if best_split["info_gain"]>0:
                # cria a árvore esquerda
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth+1)
                # cria a árvore direita
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth+1)
                # retorna o nó de decisão
                return Node(best_split["feature_index"], best_split["threshold"], 
                            left_subtree, right_subtree, best_split["info_gain"])
        
        # calcula o nó folha
        leaf_value = self.calculate_leaf_value(Y)
        # retorna o nó folha
        return Node(value=leaf_value)
    
    def get_best_split(self, dataset, num_samples, num_features):
        ''' encontra a melhor divisão '''
        
        # best_split é um dicionário
        best_split = {}
        max_info_gain = -float("inf") #Valor inicial um - infinito
        
        # loop para todos os recursos (features)
        for feature_index in range(num_features):
            feature_values = dataset[:, feature_index]
            possible_thresholds = np.unique(feature_values)
            # Loop para todos os valores presentes nos dados
            for threshold in possible_thresholds:
                # pegar divisão atual
                dataset_left, dataset_right = self.split(dataset, feature_index, threshold)
                # Verifica se os filhos não são nulos
                if len(dataset_left)>0 and len(dataset_right)>0:
                    y, left_y, right_y = dataset[:, -1], dataset_left[:, -1], dataset_right[:, -1]
                    # Computa o ganho de informação
                    curr_info_gain = self.information_gain(y, left_y, right_y, "gini")
                    # Sempre encontra a melhor divisão
                    if curr_info_gain>max_info_gain:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain
                        
        # retorna best_split
        return best_split
    
    def split(self, dataset, feature_index, threshold):
        ''' função que divide o dataset '''
        
        dataset_left = np.array([row for row in dataset if row[feature_index]<=threshold])
        dataset_right = np.array([row for row in dataset if row[feature_index]>threshold])
        return dataset_left, dataset_right
    
    def information_gain(self, parent, l_child, r_child, mode="entropy"):
        ''' função que calcula o ganho de informação '''
        
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        if mode=="gini":
            gain = self.gini_index(parent) - (weight_l*self.gini_index(l_child) + weight_r*self.gini_index(r_child))
        else:
            gain = self.entropy(parent) - (weight_l*self.entropy(l_child) + weight_r*self.entropy(r_child))
        return gain
    
    def entropy(self, y):
        ''' Entropia '''
        
        class_labels = np.unique(y)
        entropy = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            entropy += -p_cls * np.log2(p_cls)
        return entropy
    
    def gini_index(self, y):
        ''' Impuridade Gini '''
        
        class_labels = np.unique(y)
        gini = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            gini += p_cls**2
        return 1 - gini
        
    def calculate_leaf_value(self, Y):
        ''' calcula o nó folha '''
        
        Y = list(Y)
        return max(Y, key=Y.count)
    
    def print_tree(self, tree=None, indent=" ", col_name=None, results=None):
        ''' impressão da árvore '''
        
        if not tree:
            tree = self.root

        if tree.value is not None:
            print(' ',results[int(tree.value) - 1])

        else:
            print(col_name[tree.feature_index], "<=", tree.threshold, "?", " info gain: {:.2f}".format(tree.info_gain))           
            print("%sleft:" % (indent), end="")
            self.print_tree(tree.left, indent + indent, col_name=col_name, results=results)
            print("%sright:" % (indent), end="")
            self.print_tree(tree.right, indent + indent, col_name=col_name, results=results)
    
    def fit(self, X, Y):
        ''' inicia a árvore '''
        
        dataset = np.concatenate((X, Y), axis=1)
        self.root = self.build_tree(dataset)
    
    def predict(self, X):
        ''' realiza uma previsão '''
        
        preditions = [self.make_prediction(x, self.root) for x in X]
        return preditions
    
    def make_prediction(self, x, tree):
        ''' prevê um dado isolado '''
        
        if tree.value!=None: return tree.value
        feature_val = x[tree.feature_index]
        if feature_val<=tree.threshold:
            return self.make_prediction(x, tree.left)
        else:
            return self.make_prediction(x, tree.right)


col_names = ['i', 'pSist', 'pDiast', 'qPA', 'pulso', 'resp', 'gravid', 'classe']
resultados = ['crítico', 'instável', 'potencialmente estável', 'estável']
data = pd.read_csv("treino_sinais_vitais_com_label.csv", header=None, names=col_names)
print(data.head(10))


X = data.iloc[:, :-1].values
Y = data.iloc[:, -1].values.reshape(-1,1)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.2, random_state=41)

classifier = DecisionTreeClassifier(min_samples_split=4, max_depth=4)
classifier.fit(X_train,Y_train)
classifier.print_tree(col_name=col_names, results=resultados)

Y_pred = classifier.predict(X_test) 
print('Nível de precisão: ', accuracy_score(Y_test, Y_pred))
