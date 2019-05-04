import pycrfsuite
from loader import loadOCGrammasFromFile
from trainer import Trainer
from features_builder import FeaturesBuilder

"""
Тестирование всех моделей на угадывание значений
Весь текст прогоняется через модель, и считаем процент угадываний
"""

# считываем строки из файла в формате OC и переводим в граммы
filename = '../tmp/opencorpora_parsed.txt'
sentences = loadOCGrammasFromFile(filename)

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
]
for predictor in predictors:
    features_builder = FeaturesBuilder(predictor)
    errors = 0
    total = 0
    tagger = pycrfsuite.Tagger()
    tagger.open("./oc_model/crf_%s.model" % predictor)
    for sentence in sentences:
        (features, _) = features_builder.make_features_and_results(sentence)
        results = tagger.tag(features)

        for index in range(len(sentence)):
            gramma = sentence[index]
            result = results[index]
            expectedResult = getattr(gramma, predictor)
            if expectedResult == None:
                expectedResult = ""
            total += 1
            if expectedResult != result:
                # print("Error: %s %s" % (expectedResult, result))
                errors += 1
    
    print("Признак %s. Всего слов: %s. Ошибок: %s. Точность: %s" % (predictor, total, errors, round((100 - errors / total * 100), 2)))

        


