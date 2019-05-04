import pycrfsuite

class Trainer():
    def __init__(self, verbose=False):
        self.trainer = pycrfsuite.Trainer(verbose=verbose)

    def append(self, features, values):
        self.trainer.append(features, values)
    
    def train(self, filepath):
        self.trainer.select('l2sgd')
        self.trainer.train(filepath)


