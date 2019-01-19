import json
import math
from pprint import pprint

class DecisionTree:
    
    def __init__(self):
        with open('dataset.json') as f:
            self.data = json.load(f)
        self.tree = {}
        self.attr = ['twardosc', 'waga', 'wielkosc', 'ksztalt', 'skupienie']
        self.classes = ['RTV', 'Zywnosc', 'Ogrodnictwo', 'Art. Pap.', 'odziez']
        
    def addNodeToTree(self, choosen, endPoint):
        self.tree[choosen[0], choosen[1], choosen[2], choosen[3], choosen[4]] = endPoint

    def getAllResults(self, choosen):
        results = []
        for el in self.data:
            isGood = True
            if choosen[0] != '':
                if el[self.attr[0]] != choosen[0]:
                    isGood = False
            
            if choosen[1] != '':
                if el[self.attr[1]] != choosen[1]:
                    isGood = False
            
            if choosen[2] != '':
                if el[self.attr[2]] != choosen[2]:
                    isGood = False
            
            if choosen[3] != '':
                if el[self.attr[3]] != choosen[3]:
                    isGood = False
            
            if choosen[4] != '':
                if el[self.attr[4]] != choosen[4]:
                    isGood = False
                    
            if isGood:
                if el['typ'] not in results:
                    results.append(el['typ'])
        return results
        
    def getAllOptions(self, choosen, root):
        options = []
        for el in self.data:
            isGood = True
            if choosen[0] != '':
                if el[self.attr[0]] != choosen[0]:
                    isGood = False
            
            if choosen[1] != '':
                if el[self.attr[1]] != choosen[1]:
                    isGood = False
            
            if choosen[2] != '':
                if el[self.attr[2]] != choosen[2]:
                    isGood = False
            
            if choosen[3] != '':
                if el[self.attr[3]] != choosen[3]:
                    isGood = False
            
            if choosen[4] != '':
                if el[self.attr[4]] != choosen[4]:
                    isGood = False
            
            if el[self.attr[root]] not in options and isGood:
                options.append(el[self.attr[root]])
        return options
    
    def getAllOptionsForAttr(self, choosen, attr):
        options = []
        for el in self.data:
            isGood = True
            for x in range(0, 5):
                if choosen[x] == '':
                    continue
                else:
                    if el[self.attr[x]] != choosen[x]:
                        isGood = False
            if isGood:
                if el[self.attr[attr]] not in options:
                    options.append(el[self.attr[attr]])
        return options
            
    def getNextNode(self, choosen):
        i = 0
        gain = 0
        actual = 0
        while i < len(choosen):
            if choosen[i] == '':
                temp = self.gain(choosen, i)
                if temp > gain:
                    gain = temp
                    actual = i
            i += 1
        return actual
                    
    def getCountOfChoosen(self, choosen):
        count = 0
        isGood = True
        for el in self.data:
            isGood = True
            for x in range(0, 5):
                if choosen[x] == '':
                    continue
                else:
                    if el[self.attr[x]] != choosen[x]:
                        isGood = False
                        break
            if isGood:
                count += 1
        return count
        
    def getCountOfChoosenClass(self, choosen, endPoint):
        count = 0
        for el in self.data:
            isGood = True
            for x in range(0, 5):
                if choosen[x] == '':
                    continue
                else:
                    if el[self.attr[x]] != choosen[x]:
                        isGood = False
            if isGood:
                if el['typ'] == self.classes[endPoint]:
                    count += 1
        return count
    
    def entropy(self, choosen):
        entropy = 0
        count = self.getCountOfChoosen(choosen)
        ent = 0
        for x in range(0, 5):
            p_x = self.getCountOfChoosenClass(choosen, x)/50
            if p_x == 0:
                p_x = 0.00001
            ent +=  - p_x * math.log(p_x, 2)
        return ent
    
    def gain(self, choosen, attr):
        gain = self.entropy(['','','','',''])
        options = self.getAllOptionsForAttr(choosen, attr)
        sum = 0
        for x in options:
            entOptions = choosen.copy()
            entOptions[attr] = x
            sum += 0.3 * self.entropy(entOptions) #example of probability
        return gain
    
    def choosenLength(self, choosen):
        count = 0
        for x in choosen:
            if x != '':
                count += 1
        return count
        
    
    def getTree(self, choosen):
        edges = []
        nodes = []
        if len(choosen) == 0:
            # print(choosen)
            choosen = ['','','','','']
            root = self.getNextNode(choosen) #return optimal node
            edges = self.getAllOptions(choosen, root)
            # print(edges)
            for e in edges:
                choosenCopy = choosen.copy()
                choosenCopy[root] = e
                # print(choosenCopy)
                nodes = self.getAllResults(choosenCopy)
                if len(nodes) == 1:
                    self.addNodeToTree(choosenCopy, nodes[0])
                else:
                    self.getTree(choosenCopy)
        elif self.choosenLength(choosen) < 5:
            print(choosen)
            root = self.getNextNode(choosen)
            edges = self.getAllOptions(choosen, root)
            for e in edges:
                choosenCopy = choosen.copy()
                choosenCopy[root] = e
                nodes = self.getAllResults(choosenCopy)
                if len(nodes) == 1:
                    self.addNodeToTree(choosenCopy, nodes[0])
                else:
                    self.getTree(choosenCopy)
        else:
            # print(choosen)
            nodes = self.getAllResults(choosen)
            self.addNodeToTree(choosen, nodes[0])
        
    def predict(self, choosen):
        return 0
        

if __name__ == "__main__":
    decTree = DecisionTree()
    decTree.getTree([])
    print(decTree.tree)
    # decTree.predict()
