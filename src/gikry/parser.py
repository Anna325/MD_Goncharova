import sys
from lxml import etree
import re

def parse_gikry(filename):
    print("Start to parse file %s" % filename)
    gikryFile = open(filename)
    sentences = []
    sentence = []
    lIndex = 0

    for line in gikryFile:
        lIndex += 1
        sys.stdout.write("Line num: %s \r" % lIndex)
        sys.stdout.flush()
        # пустая строка - разделитель предложений. Пустые строки могут идти подряд. Пустые предложения не пишем в итог
        # строка со словом вида:
        # 515092	0001	Председатель       	[председатель]             	Npmsn-y      	
        
        # Встречаются ненужные строки вида:
        # TEXTID=18949_1******************************77519988_1049.dat

        line = line.strip()
        if line.find("TEXTID") == 0:
            continue

        if (line == ""):
            # пустая строка. Сохраняем предложение, если оно есть
            if len(sentence) > 1: # там что-то кроме BEGIN
                sentence.append("END")
                sentences.append(sentence)
            sentence = []
            sentence.append("BEGIN")
            continue

        (word, lemma, tags) = parseWord(line)
        tags = list(tags.strip())
        tags = clearEmptyTags(tags)
        tags = ",".join(tags)
        sentence.append("%s\t%s\t%s" % (word.strip(), lemma.strip(), tags))

    print()
    print("fill lines")
    print()
    lines = []
    wIndex = 0
    for sentence in sentences:
        for word in sentence:
            wIndex += 1
            lines.append(word)
            sys.stdout.write("Word num: %s \r" % wIndex)
            sys.stdout.flush()
    print()
    print('start to join text')
    text = "\n".join(lines)
    print('finish to fill lines')
    return text

def parseWord(line):
    # 515092	0001	Председатель       	[председатель]             	Npmsn-y      	
    # 519999	   P	.
    pucntM = re.search('\d+\s*P\t(.*)', line)
    wordM = re.search(
        '\d+\s+\d+\s+(.*)\t\[(.*)\]\s*\t([\?A-Za-z\-]+)', 
            line
            )
    if wordM:
        return (wordM.group(1), wordM.group(2), wordM.group(3))
    elif pucntM:
        # это знак пунктуации
        return (pucntM.group(1), pucntM.group(1), 'X')
    else:
        print("Unknown regexp for line \"%s\"" % line)
        quit()

"""
Очищаем пустые теги в конце списка тегов. Пустые теги: "-"
"""
def clearEmptyTags(tags):
    # ищем последний тег, который не пустой
    normalIndex = -1
    for index in range(len(tags)):
        if tags[index] != '-':
            normalIndex = index
    if normalIndex >= 0:
        return tags[0:normalIndex+1]
    else:
        return []




        
