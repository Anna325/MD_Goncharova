import pycrfsuite
from src.training.features_builder import FeaturesBuilder
import os

class GIKRYPredictor():
    def __init__(self, tagType, additionalTag = None):
        self.tagType = tagType
        self.tagger = pycrfsuite.Tagger()
        self.tagger.open(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'gikry', "crf_%s.model" % tagType)
        )
        self.featuresBuilder = FeaturesBuilder(tagType, additionalTag)
        
    def predict(self, sentence, index):
        (features, _) = self.featuresBuilder.make_features_and_results(sentence)
        results = self.tagger.tag(features)
        return results[index]