import collections
import os

TAGS_ORDER = [
    '-',
    's',
    'spro',
    'praedicpro',
    'apro',
    'a',
    'anum',
    'num',
    'advpro',
    'adv',
    'praedic',
    'parenth',
    'v',
    'conj',
    'pr',
    'intj',
    'part',
    'nonlex',
    'init',

    'm',
    'f',
    'n',
    'm-f',
    'anim',
    'inan',
    'sg',
    'pl',
    'nom',
    'voc',
    'gen',
    'gen2',
    'adnum',
    'dat',
    'dat2',
    'acc',
    'acc2',
    'loc',
    'loc2',
    'ins',
    'brev',
    'plen',
    'ipf',
    'pf',
    'indic',
    'imper',
    'imper2',
    '1p',
    '2p',
    '3p',
    'praet',
    'praes',
    'fut',
    'inf',
    'partcp',
    'ger',
    'act',
    'med',
    'pass',
    'comp',
    'comp2',
    'supr',
    'patrn',
    'zoon',
    'persn',
    'famn',
    'tran',
    'intr',
]

class NKRYSaver():
    def save(self, filename, sentences):
        with open(filename, 'w') as targetFile:
            for sentence in sentences:
                targetFile.write("BEGIN\n")
                for gramma in sentence:
                    string = self.grammaToString(gramma)
                    targetFile.write(string)
                targetFile.write("ENDN\n")

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
