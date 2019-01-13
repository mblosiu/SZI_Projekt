import json
from pprint import pprint

class DecisionTree:
    
    def __init__(self):
        with open('dataset.json') as f:
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

    def predict(self, choosen):
        attr = []
        for i in range(0, 5):
            attr.append(choosen[i])
            try:
                if i == 0:
                    type = self.tree[attr[0]]
                if i == 1:
                    type = self.tree[attr[0], attr[1]]
                if i == 2:
                    type = self.tree[attr[0], attr[1], attr[2]]
                if i == 3:
                    type = self.tree[attr[0], attr[1], attr[2], attr[3]]
                if i == 4:
                    type = self.tree[attr[0], attr[1], attr[2], attr[3], attr[4]]
                return type
            except KeyError:
                type = ''
        return 'error'

if __name__ == "__main__":
    with open('dataset.json') as f:
        data = json.load(f)
        
    tree = DecisionTree()
    tree.getTree([])

    true = 0
    false = 0
    error = 0

    for el in data:
        choosen = []
        choosen.append(el['twardosc'])
        choosen.append(el['waga'])
        choosen.append(el['wielkosc'])
        choosen.append(el['ksztalt'])
        choosen.append(el['skupienie'])
        type = tree.predict(choosen)
        if type == el['typ']:
            true += 1
        elif type == 'error':
            error += 1
        else:
            false += 1
            print(type, el['typ'])
    print('true: ', true)
    print('false:', false)
    print('error:', error)
    
    tw = ['twarde', 'miekkie', 'kruche']
    wa = ['ciezkie', 'lekkie', 'srednie']
    wi = ['male', 'srednie']
    ksz = ['prostokatny', 'okragly', 'kolisty', 'brak', ]
    sk = ['stale', 'ciekly']
    
    true = 0
    false = 0
    error = 0
    
    for el1 in tw:
        for el2 in wa:
            for el3 in wi:
                for el4 in ksz:
                    for el5 in sk:
                        wyb = []
                        wyb.append(el1)
                        wyb.append(el2)
                        wyb.append(el3)
                        wyb.append(el4)
                        wyb.append(el5)
                        
                        type = tree.predict(wyb)
                        if type == 'error':
                            error += 1
                            print(wyb)
                        else:
                            true += 1
                            
    print('true: ', true)
    print('errors: ', error)
    print(tree.tree)