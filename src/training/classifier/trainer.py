from sklearn.model_selection import train_test_split
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, LSTM, InputLayer, Bidirectional, TimeDistributed, Embedding, Activation
from keras.optimizers import Adam
import numpy as np
import os
import json

class ClassifierTrainer():
    def __init__(self, sentences, tag):
        self.tag = tag
        (self.sentences, self.sentences_tags) = self.buildSentencesAndTags(sentences)

        self.word2Index = {}
        self.tag2Index = {}
        self.buildIndexes()
        self.MAX_LENGTH = 0

    def buildSentencesAndTags(self, grammasSentences):
        sentences = []
        sentences_tags = []
        for grammaSentence in grammasSentences:
            sentence = []
            tags = []
            for gramma in grammaSentence:
                sentence.append(gramma.word.lower())
                tagValue = getattr(gramma, self.tag)
                if isinstance(tagValue, list):
                    tagValue = ",".join(tagValue)
                tags.append(tagValue)
            sentences.append(sentence)
            sentences_tags.append(tags)

        return sentences, sentences_tags

    def buildIndexes(self):
        words, tags = set([]), set([])
        for sentence in self.sentences:
            for word in sentence:
                words.add(word)

        self.word2Index = {w: i + 2 for i, w in enumerate(list(words))}
        self.word2Index['-PAD-'] = 0
        self.word2Index['-OOV-'] = 1

        for sentenceTags in self.sentences_tags:
            for tag in sentenceTags:
                tags.add(tag)

        self.tag2Index = {t: i + 1 for i, t in enumerate(list(tags))}
        self.tag2Index['-PAD-'] = 0

    def prepareSequences(self):
        (train_sentences, test_sentences, train_tags, test_tags) = train_test_split(self.sentences, self.sentences_tags, test_size=0.2)
        train_sentences_X, test_sentences_X, train_tags_y, test_tags_y = [], [], [], []
        for s in train_sentences:
            s_int = []
            for word in s:
                try:
                    s_int.append(self.word2Index[word])
                except KeyError:
                    # слова нет в индексе
                    s_int.append(self.word2Index['-OOV-'])
            train_sentences_X.append(s_int)

        for s in test_sentences:
            s_int = []
            for word in s:
                try:
                    s_int.append(self.word2Index[word])
                except KeyError:
                    # слова нет в индексе
                    s_int.append(self.word2Index['-OOV-'])
            test_sentences_X.append(s_int)

        for s in train_tags:
            train_tags_y.append([self.tag2Index[t] for t in s])
        
        for s in test_tags:
            test_tags_y.append([self.tag2Index[t] for t in s])

        self.MAX_LENGTH = len(max(train_sentences_X, key=len))

        train_sentences_X = pad_sequences(train_sentences_X, maxlen=self.MAX_LENGTH, padding='post')
        test_sentences_X = pad_sequences(test_sentences_X, maxlen=self.MAX_LENGTH, padding='post')
        train_tags_y = pad_sequences(train_tags_y, maxlen=self.MAX_LENGTH, padding='post')
        test_tags_y = pad_sequences(test_tags_y, maxlen=self.MAX_LENGTH, padding='post')

        return train_sentences_X,test_sentences_X,train_tags_y,test_tags_y

    def train(self, modelSavePath):
        (train_sentences_X,test_sentences_X,train_tags_y,test_tags_y) = self.prepareSequences()

        model = Sequential()
        model.add(InputLayer(input_shape=(self.MAX_LENGTH, )))
        model.add(Embedding(len(self.word2Index), 128))
        model.add(Bidirectional(LSTM(256, return_sequences=True)))
        model.add(TimeDistributed(Dense(len(self.tag2Index))))
        model.add(Activation('softmax'))
        model.compile(loss='categorical_crossentropy', optimizer=Adam(0.001), metrics=['accuracy'])
        #model.summary()

        cat_train_tags_y = self.toCategorical(train_tags_y, len(self.tag2Index))
        # print(cat_train_tags_y)
        # quit()
        model.fit(train_sentences_X, cat_train_tags_y, batch_size=128, epochs=1, validation_split=0.2)

        scores = model.evaluate(test_sentences_X, self.toCategorical(test_tags_y, len(self.tag2Index)))
        print(f"{model.metrics_names[1]}: {scores[1] * 100}")   # acc: 99.09751977804825

        if not os.path.exists(modelSavePath):
            os.makedirs(modelSavePath)
        model.save(modelSavePath + '/model.h5')
        with open(modelSavePath + '/tag2Index.json', 'w') as outfile:
            json.dump(self.tag2Index, outfile)
        with open(modelSavePath + '/word2Index.json', 'w') as outfile:
            json.dump(self.word2Index, outfile)
        with open(modelSavePath + '/maxLength.json', 'w') as outfile:
            json.dump(self.MAX_LENGTH, outfile)
        

    def toCategorical(self, sequences, categories):
        cat_sequences = []
        for s in sequences:
            cats = []
            for item in s:
                cats.append(np.zeros(categories))
                cats[-1][item] = 1.0
            cat_sequences.append(cats)
        return np.array(cat_sequences)



        
        

