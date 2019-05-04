from src.training.trainer import Trainer
from src.training.features_builder import FeaturesBuilder
from src.common.loader import loadUDGrammasFromFile
import os

def train_all_models(filename):
    sentences = loadUDGrammasFromFile(filename)
    predictors = [
        'pos',
        'mood',
        'voice',
        'nameType',
        'poss',
        'reflex',
        'degree',
        'number',
        'case',
        'gender',
        'verbForm',
    ]
    for predictor in predictors:
        trainer = Trainer(verbose=True)
        features_builder = FeaturesBuilder(predictor)
        for sentence in sentences:
            (features, results) = features_builder.make_features_and_results(sentence)
            trainer.append(features, results)
        print("trainer %s appended. Start to train" % predictor)
        trainer.train(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'ud', 'crf_%s.model' % predictor)
        )
