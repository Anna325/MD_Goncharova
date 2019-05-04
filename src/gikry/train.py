from src.training.trainer import Trainer
from src.training.features_builder import FeaturesBuilder
from src.common.loader import loadGIKRYGrammasFromFile
import os

"""
    Нужны модели для признаков:
        часть речи
        пол
        падеж
        тип существительного
        форма прилагательного
        аспект
        парность
        время
        форма глагола
        форма причастия
        переходность
        разряд прилагательного
        синтаксический тип прилагательного
        признак части речи X
        тип предлога
        структура предлога
        разряд числительного
        форма записи числительного
        разряд местоимения
        синтаксический тип местоимения
"""
def train_all_models(filename):
    sentences = loadGIKRYGrammasFromFile(filename)
    predictors = [
        'pos',
        'gender',
        'case',
        'nounType',
        'fullForm',
        'aspect',
        'aspectual',
        'tense',
        'verbForm',
        'trans',
        'categoryOfAdjective',
        'syntaxType',
        'typeOfAnother',
        'typeOfAdposition',
        'structureOfAdposition',
        'categoryOfNumeral',
        'formOfNumeral',
    ]

    for predictor in predictors:
        print("start to train %s predictor" % predictor)
        trainer = Trainer(verbose=True)
        features_builder = FeaturesBuilder(predictor)
        for sentence in sentences:
            (features, results) = features_builder.make_features_and_results(sentence)
            trainer.append(features, results)
        print("trainer %s appended. Start to train" % predictor)
        trainer.train(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'gikry', "crf_%s.model" % predictor)
        )