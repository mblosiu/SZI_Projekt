#import neurolab as nl
import json
import keras
from keras.models import Sequential
from keras.layers import Dense
import numpy


class NeuralNetwork:

    def __init__(self):
        with open('dataset.json') as f:
            self.data = json.load(f)
        learnData = []
        types = []
        for el in self.data:
            tw = 0
            wg = 0
            wlk = 0
            ksz = 0
            sk = 0
            typ = 0

            if el['twardosc'] == 'twarde':
                tw = 0
            if el['twardosc'] == 'miekkie':
                tw = 1
            if el['twardosc'] == 'kruche':
                tw = 2

            if el['waga'] == 'ciezkie':
                wg = 0
            if el['waga'] == 'lekkie':
                wg = 1
            if el['waga'] == 'srednie':
                wg = 2

            if el['wielkosc'] == 'male':
                wlk = 0
            if el['wielkosc'] == 'srednie':
                wlk = 1

            if el['ksztalt'] == 'prostokatny':
                ksz = 0
            if el['ksztalt'] == 'okragly':
                ksz = 1
            if el['ksztalt'] == 'kolisty':
                ksz = 2
            if el['ksztalt'] == 'brak':
                ksz = 3

            if el['skupienie'] == 'stale':
                sk = 0
            if el['skupienie'] == 'ciekly':
                sk = 1

            if el['typ'] == 'Leki':
                typ = [6]
            if el['typ'] == 'Zywnosc':
                typ = [1]
            if el['typ'] == 'RTV':
                typ = [0]
            if el['typ'] == 'odziez':
                typ = [4]
            if el['typ'] == 'Ogrodnictwo':
                typ = [2]
            if el['typ'] == 'Art. Pap.':
                typ = [3]
            if el['typ'] == 'Zabawki':
                typ = [7]
            types.append(typ)
            learnData.append([tw, wg, wlk, ksz, sk])

        X = numpy.array(learnData)
        Y = numpy.array(types)

        one_hot_labels = keras.utils.to_categorical(Y, num_classes=7)
        print(one_hot_labels)

        # tworzymy model
        self.model = Sequential()
        self.model.add(Dense(5, activation='relu', input_dim=5))
        self.model.add(Dense(7, activation='softmax'))
        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])
        # keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
        # Fit the model
        self.model.fit(X, one_hot_labels, epochs=10000, batch_size=85)

    def predict(self, tw, wg, wlk, ksz, sk):
        tw1 = 0
        wg1 = 0
        wlk1 = 0
        ksz1 = 0
        sk1 = 0

        if tw == 'twarde':
            tw1 = 0
        elif tw == 'miekkie':
            tw1 = 1
        elif tw == 'kruche':
            tw1 = 2

        if wg == 'ciezkie':
            wg1 = 0
        elif wg == 'lekkie':
            wg1 = 1
        elif wg == 'srednie':
            wg1 = 2

        if wlk == 'male':
            wlk1 = 0
        elif wlk == 'srednie':
            wlk1 = 1

        if ksz == 'prostokatny':
            ksz1 = 0
        elif ksz == 'okragly':
            ksz1 = 1
        elif ksz == 'kolisty':
            ksz1 = 2
        elif ksz == 'brak':
            ksz1 = 3

        if sk == 'stale':
            sk1 = 0
        elif  sk == 'ciekly':
            sk1 = 1

        item = []
        item.append([tw1, wg1, wlk1, ksz1, sk1])
        X = numpy.array(item)
        prediction = self.model.predict_classes(X)
        indexklasy = prediction[0]

        if (indexklasy == 0):
            typ = 'RTV'
        if (indexklasy == 1):
            typ = 'Zywnosc'
        if (indexklasy == 2):
            typ = 'Ogrodnictwo'
        if (indexklasy == 3):
            typ = 'Art. Pap.'
        if (indexklasy == 4):
            typ = 'odziez'
        if (indexklasy == 5):
            typ = 'Leki'

        return typ

    def test(self):
        with open('dataset.json') as f:
            data = json.load(f)
        for el in data:
            print(self.predict(el['twardosc'], el['waga'], el['wielkosc'], el['ksztalt'], el['skupienie']))

if __name__ == "__main__":
    NN = NeuralNetwork()
    NN.test()

