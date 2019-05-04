import sys
from lxml import etree

def parse_nkry(filename):
    print("Start to parse file %s" % filename)
   
    nkryFile = open(filename)
    text = nkryFile.read()
    text = text.replace('encoding="windows-1251"', '')
    tree = etree.fromstring(text)
    print("Finish parse file %s" % filename)
    lines = []

    pIndex = 1

    for sentence in tree.iter('se'):
        sys.stdout.write("sentence num: %s \r" % pIndex)
        sys.stdout.flush()
        pIndex += 1
        lines.append("BEGIN")
        for wordTag in sentence.iter('w'):
            word = None
            lemma=None
            tags=None
            for ana in wordTag.iter('ana'):
                # ana = word.find('ana')
                if ana.tail:
                    word = ana.tail
                if not word:
                    continue
                word = word.replace('`', '')
                lemma = ana.get('lex')
                tags = ana.get('gr')
            if not word or not lemma or not tags:
                continue
            lines.append("%s\t%s\t%s" % (word.strip(), lemma.strip(), tags.strip().replace('=', ',').replace('-', '')))
        lines.append("END")
    print()
    return "\n".join(lines)