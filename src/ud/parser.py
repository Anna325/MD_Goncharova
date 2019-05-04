import sys

def parse_ud(filename):
    print("Start to parse file %s" % filename)
    udFile = open(filename)
    lines = []

    lines.append('BEGIN')
    for line in udFile:
        line = line.strip()
        if line.find('==') == 0:
            continue # техническая строка
        if not line or line.strip() == '':
            # Новое предложение
            lines.append('END')
            lines.append('BEGIN')
        else:
            items = line.split("\t")
            word = items[0].strip()
            lemma = items[1].strip()
            PoS = items[2].strip()
            tags1 = items[3].strip() if len(items) > 3 else ""
            tags2 = items[4].strip() if len(items) > 4 else ""

            tags = [PoS]
            if tags1 != '_':
                tags.extend(tags1.split('|'))
            if tags2 != '_':
                tags.extend(tags2.split('|'))
            
            lines.append("%s\t%s\t%s" % (word, lemma, ",".join(tags)))
    lines.append('END')

    return "\n".join(lines)

    

    