import json
from pprint import pprint

class DecisionTree:
    
    def __init__(self):
        with open('dataset2.json') as f:
            self.data = json.load(f)
        self.tree = {}
            
    def getAllOptions(self, choosen):
        options = []
        count = len(choosen)
        if count == 0:
            for el in self.data:
                if el['twardosc'] not in options:
                    options.append(el['twardosc'])
        else:
            if count == 1:
                for el in self.data:
                    if el['twardosc'] == choosen[0]:
                        if el['waga'] not in options:
                            options.append(el['waga'])
            elif count == 2:
                for el in self.data:
                    if el['twardosc'] == choosen[0] and el['waga'] == choosen[1]:
                        if el['wielkosc'] not in options:
                            options.append(el['wielkosc'])
            elif count == 3:
                for el in self.data:
                    if el['twardosc'] == choosen[0] and el['waga'] == choosen[1] and el['wielkosc'] == choosen[2]:
                        if el['ksztalt'] not in options:
                            options.append(el['ksztalt'])
            elif count == 4:
                for el in self.data:
                    if el['twardosc'] == choosen[0] and el['waga'] == choosen[1] and el['wielkosc'] == choosen[2] and el['ksztalt'] == choosen[3]:
                        if el['skupienie'] not in options:
                            options.append(el['skupienie'])
            
        return options

    def getAllResults(self, choosen):
        results = []
        count = len(choosen)
        if count == 1:
            for el in self.data:
                if el['twardosc'] == choosen[0]:
                    if el['typ'] not in results:
                        results.append(el['typ'])
        elif count == 2:
            for el in self.data:
                if el['twardosc'] == choosen[0] and el['waga'] == choosen[1]:
                    if el['typ'] not in results:
                        results.append(el['typ'])
        elif count == 3:
            for el in self.data:
                if el['twardosc'] == choosen[0] and el['waga'] == choosen[1] and el['wielkosc'] == choosen[2]:
                    if el['typ'] not in results:
                        results.append(el['typ'])
        elif count == 4:
            for el in self.data:
                if el['twardosc'] == choosen[0] and el['waga'] == choosen[1] and el['wielkosc'] == choosen[2] and el['ksztalt'] == choosen[3]:
                    if el['typ'] not in results:
                        results.append(el['typ'])
        elif count == 5:
            for el in self.data:
                if el['twardosc'] == choosen[0] and el['waga'] == choosen[1] and el['wielkosc'] == choosen[2] and el['ksztalt'] == choosen[3] and el['skupienie'] == choosen[4]:
                    if el['typ'] not in results:
                        results.append(el['typ'])
            
        return results
        
    def addNodeToTree(self, choosen, endPoint):
        count = len(choosen)
        if count == 2:
            self.tree[choosen[0], choosen[1]] = endPoint
        elif count == 3:
            self.tree[choosen[0], choosen[1], choosen[2]] = endPoint
        elif count == 4:
            self.tree[choosen[0], choosen[1], choosen[2], choosen[3]] = endPoint
        elif count == 5:
            self.tree[choosen[0], choosen[1], choosen[2], choosen[3], choosen[4]] = endPoint
            
    def getTree(self, choosen):
        edges = []
        nodes = []
        if len(choosen) == 0:
            edges = self.getAllOptions(choosen)
            for e in edges:
                singleNode = []
                singleNode.append(e)
                nodes = self.getAllResults(singleNode)
                if len(nodes) == 1:
                    self.tree[e] = nodes[0]
                else:
                    next = choosen.copy()
                    next.append(e)
                    self.getTree(next)
        elif len(choosen) < 5:
            edges = self.getAllOptions(choosen)
            for e in edges:
                newChoosen = choosen.copy()
                newChoosen.append(e)
                nodes = self.getAllResults(newChoosen)
                if len(nodes) == 1:
                    self.addNodeToTree(newChoosen, nodes[0])
                else:
                    next = choosen.copy()
                    next.append(e)
                    self.getTree(next)
        else:
            nodes = self.getAllResults(choosen)
            if len(nodes) > 0:
                self.addNodeToTree(choosen, nodes[0])

t = DecisionTree()
t.getTree([])
print(t.tree)