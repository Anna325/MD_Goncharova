from keras.models import Sequential
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding, Activation
from keras.optimizers import Adam
from keras.preprocessing.sequence import pad_sequences
import numpy as np
import json

class NnPredictor():
    def __init__(self, markupName, tag):
        self.markupName = markupName
        self.tag = tag
        with open('model/%s/classifier/%s/maxLength.json' % (self.markupName, self.tag), 'r') as maxLengthFile:
            self.MAX_LENGTH = json.load(maxLengthFile)
        with open('model/%s/classifier/%s/tag2Index.json' % (self.markupName, self.tag), 'r') as tag2IndexFile:
            self.tag2Index = json.load(tag2IndexFile)        
        with open('model/%s/classifier/%s/word2Index.json' % (self.markupName, self.tag), 'r') as word2IndexFile:
            self.word2Index = json.load(word2IndexFile)        

        model = Sequential()
        model.add(InputLayer(input_shape=(self.MAX_LENGTH, )))
        model.add(Embedding(len(self.word2Index), 128))
        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(TimeDistributed(Dense(len(self.tag2Index))))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(0.001), metrics=['accuracy'])
        model.load_weights("model/%s/classifier/%s/model.h5" % (self.markupName, self.tag))
        self.model = model

    def predict(self, sentences):
        sequences = self.prepareFeatures(sentences)
        print("Start prediction")
        predictions = self.model.predict(sequences, batch_size=256, verbose=True)
        print("Finish prediction")
        index = {i: t for t, i in self.tag2Index.items()}
        tokens = self.logitsToTokens(predictions, index)
        return tokens

    def prepareFeatures(self, sentences):
        sequences = []
        for sentence in sentences:
            s_int = []
            for gramma in sentence:
                word = gramma.word
                try:
                    s_int.append(self.word2Index[word])
                except KeyError:
                    s_int.append(self.word2Index['-OOV-'])
            words = [g.word for g in sentence]
            sequences.append(s_int)
       
        sequences = pad_sequences(sequences, maxlen=self.MAX_LENGTH, padding='post')
        return sequences
        
    def logitsToTokens(self, sequences, index):
        token_sequences = []
        for categorical_sequence in sequences:
            token_sequence = []
            for categorical in categorical_sequence:
                token_sequence.append(index[np.argmax(categorical)])
    
            token_sequences.append(token_sequence)
    
        return token_sequences


