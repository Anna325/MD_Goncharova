class FeaturesBuilder():
    def __init__(self, param, additionalTag = None):
        self.param = param
        self.additionalTag = additionalTag

    def make_features_and_results(self, sentence):
        featuresList = []
        resultsList = []
        for index in range(len(sentence)):
            gramma = sentence[index]
            features = {
                'word': gramma.word,
            }
            if len(gramma.word) > 3:
                features['word_ending'] = gramma.word[-3:]
            if index > 0:
                prevGramma = sentence[index-1]
                features['prev_word'] = prevGramma.word
            else:
                features['BEGIN'] = True

            if index < len(sentence) - 1:
                nextGramma = sentence[index+1]
                features['next_word'] = nextGramma.word
            else:
                features['END'] = True

            featuresList.append(features)
            if self.param == 'additional' and self.additionalTag:
                additionalTagsInGramma = gramma.additional
                if self.additionalTag in additionalTagsInGramma:
                    result = self.additionalTag
                else:
                    result = None
            else:
                result = getattr(gramma, self.param)
                if isinstance(result, list):
                    result = ",".join(result)
                
            resultsList.append(result if result != None else "")

        return featuresList, resultsList