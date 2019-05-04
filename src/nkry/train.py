from src.training.trainer import Trainer
from src.training.features_builder import FeaturesBuilder
from src.common.loader import loadNKRYGrammasFromFile
import os

"""
    Какие предсказатели нужны для конвертации UD -> NKRY:
        pos
        case
        mood
        degree
        nameType
        trans
        fullForm
"""
def train_all_models(filename):
    sentences = loadNKRYGrammasFromFile(filename)
    predictors = [
        'pos',
        'case',
        'mood',
        'degree',
        'nameType',
        'trans',
        'fullForm',
    ]

    for predictor in predictors:
        print("start to train %s predictor" % predictor)
        trainer = Trainer(True)
        features_builder = FeaturesBuilder(predictor)
        for sentence in sentences:
            (features, results) = features_builder.make_features_and_results(sentence)
            trainer.append(features, results)
        print("trainer %s appended. Start to train" % predictor)
        trainer.train(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'nkry', "crf_%s.model" % predictor)
        )