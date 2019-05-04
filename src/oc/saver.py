import collections
import os

TAGS_ORDER = [
    'unkn',
    'numb',
    'latn',
    'pnct',
    'romn',
    'symb',
    
    'post',
    'noun',
    'adjf',
    'adjs',
    'adjx',
    'comp',
    'verb',
    'infn',
    'prtf',
    'prts',
    'grnd',
    'numr',
    'advb',
    'npro',
    'pred',
    'prep',
    'conj',
    'prcl',
    'intj',
    'anim',
    'anim',
    'inan',
    'gndr',
    'masc',
    'femn',
    'neut',
    'ms-f',
    'nmbr',
    'sing',
    'plur',
    'sgtm',
    'pltm',
    'fixd',
    'case',
    'nomn',
    'gent',
    'datv',
    'accs',
    'ablt',
    'loct',
    'voct',
    'gen1',
    'gen2',
    'acc2',
    'loc1',
    'loc2',
    'abbr',
    'name',
    'surn',
    'patr',
    'geox',
    'orgn',
    'trad',
    'subx',
    'supr',
    'qual',
    'apro',
    'anum',
    'poss',
    'v-ey',
    'v-oy',
    'cmp2',
    'v-ej',
    'aspc',
    'perf',
    'impf',
    'impx',
    'trns',
    'tran',
    'intr',
    'impe',
    'uimp',
    'mult',
    'refl',
    'pers',
    '1per',
    '2per',
    '3per',
    'tens',
    'pres',
    'past',
    'futr',
    'mood',
    'indc',
    'impr',
    'invl',
    'incl',
    'excl',
    'voic',
    'actv',
    'pssv',
    'infr',
    'slng',
    'arch',
    'litr',
    'erro',
    'dist',
    'ques',
    'dmns',
    'prnt',
    'v-be',
    'v-en',
    'v-ie',
    'v-bi',
    'fimp',
    'prdx',
    'coun',
    'coll',
    'v-sh',
    'af-p',
    'inmx',
    'vpre',
    'anph',
    'init',
]

class OCSaver():
    def save(self, filename, sentences):
        with open(filename, 'w') as targetFile:
            for sentence in sentences:
                targetFile.write("BEGIN\n")
                for gramma in sentence:
                    string = self.grammaToString(gramma)
                    targetFile.write(string)
                targetFile.write("END\n")

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
