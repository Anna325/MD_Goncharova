from src.common.gramma import Gramma
import operator

class GrammaDiffer():
    def __init__(self):
        self.tags = [
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
            'additional',
            'fullForm',
            'nounType',
            'additionalCase',
            'aspectual',
            'categoryOfAdjective',
            'syntaxType',
            'categoryOfNumeral',
            'formOfNumeral',
            'typeOfAdposition',
            'structureOfAdposition',
            'typeOfAnother',
        ]
        self.errors = {}
        self.errorsCount = 0
        self.totalCount = 0
        
    def registerPair(self, originalGramma: Gramma, reconvertedGramma: Gramma):
        for tag in self.tags:
            originalAttr = getattr(originalGramma, tag)
            if originalAttr == '-':
                originalAttr = None
            reconvertedAttr = getattr(reconvertedGramma, tag)
            if reconvertedAttr == '-':
                reconvertedAttr = None
            if (originalAttr != reconvertedAttr ):
                # print("%s: %s. %s -> %s" % (originalGramma.pos, tag, originalAttr, reconvertedAttr))
                if not tag in self.errors:
                    self.errors[tag] = 0
                self.errors[tag] += 1
                self.errorsCount += 1
            
            self.totalCount += 1

    def dumpResult(self):
        sorted_d = sorted(self.errors.items(), key=operator.itemgetter(1))
        for (error, num) in sorted_d:
            print("Error in tag %s, errors count: %s" % (error, num))
        print("Total: %s. Errors: %s. Accuracy: %s" % (self.totalCount, self.errorsCount, round(100 - self.errorsCount / self.totalCount * 100, 2)))

def diff_sentences(originalSentences, reconvertedSentences):
    if len(originalSentences) != len(reconvertedSentences):
        raise Exception("Original sentences and reconverted sentences length must be equals")

    grammaDiffer = GrammaDiffer()

    for index in range(len(originalSentences)):
        originalSentence = originalSentences[index]
        reconvertedSentence = reconvertedSentences[index]
        for wordIndex in range(len(originalSentence)):
            originalWord = originalSentence[wordIndex]
            reconvertedWord = reconvertedSentence[wordIndex]
            grammaDiffer.registerPair(originalWord, reconvertedWord)
    
    grammaDiffer.dumpResult()
