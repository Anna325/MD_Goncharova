from src.common.nnPredictor import NnPredictor
from src.common.loader import loadUDGrammasFromFile
from src.oc.converter_oc2ud import OC2UDConverter

def nnVsCrfTest():
    predictor = NnPredictor("oc", "pos")
    oc_sentences = loadUDGrammasFromFile('tmp/opencorpora_parsed.txt')
    # result = predictor.predict(ud_sencentes[30], 0)
    # result = predictor.predict(ud_sencentes[32], 0)
    # result = predictor.predict(ud_sencentes[33], 0)
    result = predictor.predict(oc_sentences[34], 0)
    print(result)

    # oc2udConverter = OC2UDConverter(True)


    # for sentenceIndex in range(len(oc_sentences)):
    #     sentence = oc_sentences[sentenceIndex]
    #     for grammaIndex in range(len(sentence)):
    #         gramma = sentence[grammaIndex]
            # конвертируем OC в UD

            # конвертируем UD в OC



    