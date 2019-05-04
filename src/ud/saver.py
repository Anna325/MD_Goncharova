import collections
import os

TAGS_ORDER = [
    'noun',
    'propn',
    'pron',
    'det',
    'adj',
    'num',
    'conj',
    'adv',
    'part',
    'adp',
    'aux',
    'verb',
    'intj',
    'sym',
    'punct',
    'x',
    'h', # непонятно, что это
    'gender=masc',
    'gender=fem',
    'gender=neut',
    'animacy=anim',
    'animacy=inan',
    'number=sing',
    'number=coll',
    'number=plur',
    'number=ptan',
    'case=nom',
    'case=gen',
    'case=dat',
    'case=acc',
    'case=loc',
    'case=ins',
    'aspect=imp',
    'aspect=perf',
    'mood=ind',
    'mood=cnd',
    'mood=imp',
    'person=1',
    'person=2',
    'person=3',
    'poss=yes',
    'reflex=yes',
    'tense=past',
    'tense=pres',
    'tense=fut',
    'verbform=fin',
    'verbform=inf',
    'verbform=part',
    'verbform=trans',
    'voice=act',
    'voice=mid',
    'voice=pass',
    'degree=pos',
    'degree=cmp',
    'degree=sup',
    'nametype=geo',
    'nametype=prs',
    'nametype=giv',
    'nametype=sur',
    'nametype=com',
    'nametype=pro',
    'nametype=oth',
]

class UDSaver():
    def save(self, filename, sentences):
        with open(filename, 'w') as targetFile:
            for sentence in sentences:
                targetFile.write("BEGIN\n")
                for gramma in sentence:
                    string = self.grammaToString(gramma)
                    targetFile.write(string)
                targetFile.write("END\n")
        targetFile.close()


    def grammaToString(self, gramma):
        tags = []
        tags.append(gramma.pos)
        if gramma.gender != None: tags.append(gramma.gender)
        if gramma.animacy != None: tags.append(gramma.animacy)
        if gramma.number != None: tags.append(gramma.number)
        if gramma.case != None: tags.append(gramma.case)
        if gramma.aspect != None: tags.append(gramma.aspect)
        if gramma.mood != None: tags.append(gramma.mood)
        if gramma.person != None: tags.append(gramma.person)
        if gramma.poss != None: tags.append(gramma.poss)
        if gramma.reflex != None: tags.append(gramma.reflex)
        if gramma.tense != None: tags.append(gramma.tense)
        if gramma.verbForm != None: tags.append(gramma.verbForm)
        if gramma.voice != None: tags.append(gramma.voice)
        if gramma.degree != None: tags.append(gramma.degree)
        if gramma.nameType != None: tags.append(gramma.nameType)
        if gramma.trans != None: tags.append(gramma.trans)
        if gramma.invl != None: tags.append(gramma.invl)
        tags.extend(gramma.additional)
        tags = self.sortTags(tags)

        return "%s\t%s\t%s\n" % (gramma.word, gramma.lemma, ",".join(tags))

    def sortTags(self, tags):
        tagsDict = {}
        for tag in tags:
            if not tag: 
                continue
            index = TAGS_ORDER.index(tag.lower())
            tagsDict[index] = tag
        tagsDict = collections.OrderedDict(sorted(tagsDict.items()))
        sortedTags = []
        for key, value in tagsDict.items():
            sortedTags.append(value)
        return sortedTags
