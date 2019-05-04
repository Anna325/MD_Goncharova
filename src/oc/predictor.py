import pycrfsuite
from src.training.features_builder import FeaturesBuilder
import os


class OCPrecitor():
    def __init__(self, tagType, additionalTag = None):
        self.tagType = tagType
        self.tagger = pycrfsuite.Tagger()
        
        if False and tagType == 'additional':
            self.tagger.open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'oc', "crf_additional_%s.model" % additionalTag)
            )
        else:
            self.tagger.open(
                os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'oc', "crf_%s.model" % tagType)
            )
        self.featuresBuilder = FeaturesBuilder(tagType, additionalTag)
        
    def predict(self, sentence, index):
        (features, _) = self.featuresBuilder.make_features_and_results(sentence)
        results = self.tagger.tag(features)
        return results[index]