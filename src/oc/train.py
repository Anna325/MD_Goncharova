from src.training.trainer import Trainer
from src.common.loader import loadOCGrammasFromFile
from src.training.features_builder import FeaturesBuilder
import os
"""
Обучение всех моделей для всех признаков
"""

def train_all_models(filename):
    # считываем строки из файла в формате OC и переводим в граммы    
    sentences = loadOCGrammasFromFile(filename)

    # создаем тренера и загружаем грамемы (предложения) в него

    predictors = [
        'pos',
        'gender',
        'animacy',
        'number',
        'case',
        'aspect',
        'mood',
        'person',
        'poss',
        'reflex',
        'tense',
        'verbForm',
        'voice',
        'degree',
        'nameType',
        'trans',
        'invl',
        'additional' # Дополнительные теги учим по одному
    ]
    for predictor in predictors:
        print("start to train %s" % predictor)
        trainer = Trainer(verbose=True)
        features_builder = FeaturesBuilder(predictor)
        for sencence in sentences:
            (features, results) = features_builder.make_features_and_results(sencence)
            trainer.append(features, results)
        print("trainer %s appended. Start to train" % predictor)
        trainer.train(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'oc', "crf_%s.model" % predictor)
        )

    # отдельные теги быстро учатся, но плохо и долго работают. не учим отдельно
    # additionalTags = [
    #     'Infr',
    #     'Slng',
    #     'Arch',
    #     'Litr',
    #     'Erro',
    #     'Dist',
    #     'Ques',
    #     'Dmns',
    #     'Prnt',
    #     'V-be',
    #     'V-en',
    #     'V-ie',
    #     'V-bi',
    #     'V-ey',
    #     'V-oy',
    #     'Coun',
    #     'Af-p',
    #     'Anph',
    #     'Subx',
    #     'Vpre',
    #     'Prdx',
    #     'Coll',
    #     'Adjx',
    #     'Qual',
    #     'Apro',
    #     'Anum',
    #     'Poss',
    #     'ms-f',
    #     'Ms-f',
    #     'Impe',
    #     'Impx',
    #     'Mult',
    #     'Abbr',
    #     'Fixd',
    # ]

    # for additionalTag in additionalTags:
    #     print("start to train additional tag %s" % additionalTag)
    #     trainer = Trainer()
    #     features_builder = FeaturesBuilder('additional', additionalTag)
    #     for sentence in sentences:
    #         (features, results) = features_builder.make_features_and_results(sentence)
    #         trainer.append(features, results)
    #     print("trainer additiona - %s appended. Start to train" % additionalTag)
    #     trainer.train(
    #         os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'model', 'oc', "crf_additional_%s.model" % additionalTag)
    #     )