"""
Сборщик статистики по ошибкам
"""
import operator

class ErrStats():
    def __init__(self):
        self.errors = {}

    def registerError(self, normalTags, predictedTags):
        if normalTags and predictedTags:
            missingTags = list(set(normalTags) - set(predictedTags))
            extraTags = list(set(predictedTags) - set(normalTags))    
        elif not normalTags and predictedTags and len(predictedTags) > 0:
            extraTags = predictedTags
            missingTags = []
        elif not predictedTags and normalTags and len(normalTags) > 0:
            missingTags = normalTags
            extraTags = []
        else:
            raise Exception("No normal tags and no predicted tags")
        
        actualTags = []
        for missingTag in missingTags:
            actualTags.append("-%s" % missingTag)
        for extraTag in extraTags:
            actualTags.append("+%s" % extraTag)

        string = ",".join(actualTags)
        if not string in self.errors:
            self.errors[string] = 0
        self.errors[string] += 1

    def printErrors(self):
        sorted_d = sorted(self.errors.items(), key=operator.itemgetter(1))
        for (error, num) in sorted_d:
            print("Error: %s, number: %s" % (error, num))
        

    