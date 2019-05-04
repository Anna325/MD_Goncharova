import sys
import xml.etree.ElementTree as ET
import src.oc.oc_tags as OCTags
import collections
"""
Парсинг XML-файла OpenCorpora в строчную структуру
"""

def parse_opencorpora(filename):
    print("Start to parse file")
    tree = ET.parse(filename)
    print("Finish parse file")
    root = tree.getroot()
    lines = []

    pIndex = 1
    for text in root:
        for paragraph in text.iter('paragraphs'):
            sys.stdout.write("Paragraph num: %s \r" % pIndex)
            sys.stdout.flush()
            pIndex += 1
            for sentence in paragraph:
                lines.append("BEGIN")
                for tokens in sentence.iter("tokens"):
                    for token in tokens:
                        tokenStr = parse_token(token)
                        lines.append(tokenStr)
                lines.append("END")
    print()
    return "\n".join(lines)
                

"""
    Парсинг <token id="2" text="Школа"><tfr rev_id="834910" t="Школа"><v><l id="380220" t="школа"><g v="NOUN"/><g v="inan"/><g v="femn"/><g v="sing"/><g v="nomn"/></l></v></tfr></token>
    в Школа школа NOUN,inan,femn,sing,nomn
"""
def parse_token(token):
    word = token.attrib['text']
    v = token.find('tfr').find('v')
    lemma = v.find('l').attrib['t']
    tags = [g.attrib['v'] for g in v.iter('g')]
    tags = sort_tags(tags)
    # tags = normalize_tags(tags)
    return word + "\t" + lemma + "\t" + ",".join(tags)

"""
Выкинуть ненужные теги и оставить нужные.
Массив тегов должен быть всегда одной длины, с пропусками значений, если они не найдены

POST - часть речи
ANim - категория одушевлённости
GNdr - род / род не выражен
NMbr - число
CAse - 	категория падежа
ASpc - категория вида
TRns - 	категория переходности
PErs - 	категория лица
TEns - категория времени
MOod - категория наклонения
INvl - категория совместности
VOic - категория залога
"""
def normalize_tags(tags):
    normalized_tags = [""] * 12
    for tag in tags:
        if tag in OCTags.post:
            normalized_tags[0] = tag
        if tag in OCTags.anim:
            normalized_tags[1] = tag
        if tag in OCTags.gndr:
            normalized_tags[2] = tag
        if tag in OCTags.nmbr:
            normalized_tags[3] = tag
        if tag in OCTags.case:
            normalized_tags[4] = tag
        if tag in OCTags.aspc:
            normalized_tags[5] = tag
        if tag in OCTags.trns:
            normalized_tags[6] = tag
        if tag in OCTags.pers:
            normalized_tags[7] = tag
        if tag in OCTags.tens:
            normalized_tags[8] = tag
        if tag in OCTags.mood:
            normalized_tags[9] = tag
        if tag in OCTags.invl:
            normalized_tags[10] = tag
        if tag in OCTags.voic:
            normalized_tags[11] = tag
    return normalized_tags

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
def sort_tags(tags):
    tagsDict = {}
    for tag in tags:
        index = TAGS_ORDER.index(tag.lower())
        tagsDict[index] = tag
    tagsDict = collections.OrderedDict(sorted(tagsDict.items()))
    sortedTags = []
    for key, value in tagsDict.items():
        sortedTags.append(value)
    return sortedTags