import collections
import os
from src.common.gramma import Gramma

class GIKRYSaver():
    def save(self, filename, sentences):
        with open(filename, 'w') as targetFile:
            for sentence in sentences:
                targetFile.write('BEGIN\n')
                for gramma in sentence:
                    string = self.grammaToString(gramma)
                    targetFile.write("%s\n" % string)
                targetFile.write('END\n')
    
    def grammaToString(self, gramma: Gramma):
        tags = []
        tags.append(gramma.pos)
        if gramma.pos == 'N':
            tags.append(gramma.nounType)
            tags.append(gramma.gender)
            tags.append(gramma.number)
            tags.append(gramma.case)
            tags.append(gramma.additionalCase)
            tags.append(gramma.animacy)
        if gramma.pos == 'A':
            tags.append(gramma.degree)
            tags.append(gramma.gender)
            tags.append(gramma.number)
            tags.append(gramma.case)
            tags.append(gramma.fullForm)
        if gramma.pos == 'V':
            if gramma.mood:
                tags.append(gramma.mood)
            else:
                tags.append(gramma.verbForm)
            tags.append(gramma.gender)
            tags.append(gramma.number)
            tags.append(gramma.case)
            tags.append(gramma.person)
            tags.append(gramma.tense)
            tags.append(gramma.trans)
            tags.append(gramma.voice)
            tags.append(gramma.aspect)
            tags.append(gramma.aspectual)
            tags.append(gramma.fullForm)
        if gramma.pos == 'R':
            tags.append(gramma.degree)
        # if gramma.pos == 'W':
            
        if gramma.pos == 'P':
            tags.append(gramma.categoryOfAdjective)
            tags.append(gramma.gender)
            tags.append(gramma.number)
            tags.append(gramma.case)
            tags.append(gramma.person)
            tags.append(gramma.syntaxType)

        if gramma.pos == 'M':
            tags.append(gramma.categoryOfNumeral)
            tags.append(gramma.gender)
            tags.append(gramma.number)
            tags.append(gramma.case)
            tags.append(gramma.formOfNumeral)

        if gramma.pos == 'S':
            tags.append(gramma.typeOfAdposition)
            tags.append(gramma.structureOfAdposition)
            tags.append('-')
            tags.append(gramma.case)

        # if gramma.pos == 'C':

        # if gramma.pos == 'H':

        # if gramma.pos == 'I':

        # if gramma.pos == 'Q':

        if gramma.pos == 'X':
            tags.append(gramma.typeOfAnother)
        tags = ['-' if not tag else tag for tag in tags]
        tags = self.clearEmptyTags(tags)
        lemma = gramma.lemma if gramma.lemma else gramma.word
        return "%s\t%s\t%s" % (gramma.word, lemma, ",".join(tags))
    
    """
    Очищаем пустые теги в конце списка тегов. Пустые теги: "-"
    """
    def clearEmptyTags(self, tags):
        # ищем последний тег, который не пустой
        normalIndex = -1
        for index in range(len(tags)):
            if tags[index] != '-':
                normalIndex = index
        if normalIndex >= 0:
            return tags[0:normalIndex+1]
        else:
            return []
    

