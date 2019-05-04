from src.common.gramma import Gramma
"""
    Чтение файла в массив предложений, состоящих из грамем
"""

def loadOCGrammasFromFile(filename):
    with open(filename) as OC:
        sentences = []
        sentence = []
        for line in OC:
            line = line.strip()
            if line == 'BEGIN':
                sentence = []
                continue
            elif line == 'END':
                sentences.append(sentence)
                continue
            
            # « « PNCT
            # Школа школа NOUN,inan,femn,sing,nomn

            word = None
            lemma = None
            pos = None
            gender = None
            animacy = None
            number = None
            case = None
            aspect = None
            mood = None
            person = None
            poss = None
            reflex = None
            tense = None
            verbForm = None
            voice = None
            degree = None
            nameType = None
            trans = None
            invl = None
            additional = []

            lineParts = line.strip().split('\t')
            word = lineParts[0]
            lemma = lineParts[1]
            tags = lineParts[2] if lineParts[2] else ""
            tags = tags.split(",")
            pos = tags[0] if len(tags) else None
            tags = tags[1:] if len(tags) > 1 else []

            # род
            if 'masc' in tags:
                gender = 'masc'
            if 'femn' in tags:
                gender = 'femn'
            if 'neut' in tags:
                gender = 'neut'

            if 'anim' in tags:
                animacy = 'anim'
            if 'inan' in tags:
                animacy = 'inan'

            if 'sing' in tags:
                number = 'sing'
            if 'plur' in tags:
                number = 'plur'
            if 'Pltm' in tags:
                number = 'Pltm'
            if 'Sgtm' in tags:
                number = 'Sgtm'

            if 'nomn' in tags:
                case = 'nomn'
            if 'voct' in tags:
                case = 'voct'
            if 'gent' in tags:
                case = 'gent'
            if 'gen1' in tags:
                case = 'gen1'
            if 'gen2' in tags:
                case = 'gen2'
            if 'datv' in tags:
                case = 'datv'
            if 'accs' in tags:
                case = 'accs'
            if 'acc2' in tags:
                case = 'acc2'
            if 'loct' in tags:
                case = 'loct'
            if 'loc1' in tags:
                case = 'loc1'
            if 'loc2' in tags:
                case = 'loc2'
            if 'ablt' in tags:
                case = 'ablt'

            if 'impf' in tags:
                aspect = 'impf'
            if 'perf' in tags:
                aspect = 'perf'

            if 'indc' in tags:
                mood = 'indc'
            if 'impr' in tags:
                mood = 'impr'

            if '1per' in tags:
                person = '1per'
            if '2per' in tags:
                person = '2per'
            if '3per' in tags:
                person = '3per'
            
            if 'past' in tags:
                tense = 'past'
            if 'pres' in tags:
                tense = 'pres'
            if 'futr' in tags:
                tense = 'futr'

            if 'INFN' in tags:
                verbForm = 'INFN'
            if 'PRTF' in tags:
                verbForm = 'PRTF'
            if 'PRTS' in tags:
                verbForm = 'PRTS'
            if 'GRND' in tags:
                verbForm = 'GRND'
            if 'Fimp' in tags:
                verbForm = 'Fimp'
            if 'V-sh' in tags:
                verbForm = 'V-sh'

            if 'actv' in tags:
                voice = 'actv'
            if 'pssv' in tags:
                voice = 'pssv'

            if 'ADVB' in tags:
                degree = 'ADVB'
            if 'COMP' in tags and 'Cmp2' in tags:
                degree = 'COMP, Cmp2'
            if 'COMP' in tags and 'V-ej' in tags:
                degree = 'COMP, V-ej'
            if 'COMP' in tags and 'Supr' in tags:
                degree = 'COMP, Supr'

            if 'Geox' in tags:
                nameType = 'Geox'
            if 'Part' in tags:
                nameType = 'Part'
            if 'Name' in tags:
                nameType = 'Name'
            if 'Surn' in tags:
                nameType = 'Surn'
            if 'Orgn' in tags:
                nameType = 'Orgn'
            if 'Trad' in tags:
                nameType = 'Trad'
            if 'Init' in tags:
                nameType = 'Init'
            
            if 'tran' in tags:
                trans = 'tran'
            if 'intr' in tags:
                trans = 'intr'

            if 'incl' in tags:
                invl = 'tran'
            if 'excl' in tags:
                invl = 'intr'

            if 'Infr' in tags:
                additional.append('Infr')
            if 'Slng' in tags:
                additional.append('Slng')
            if 'Arch' in tags:
                additional.append('Arch')
            if 'Litr' in tags:
                additional.append('Litr')
            if 'Erro' in tags:
                additional.append('Erro')
            if 'Dist' in tags:
                additional.append('Dist')
            if 'Ques' in tags:
                additional.append('Ques')
            if 'Dmns' in tags:
                additional.append('Dmns')
            if 'Prnt' in tags:
                additional.append('Prnt')
            if 'V-be' in tags:
                additional.append('V-be')
            if 'V-en' in tags:
                additional.append('V-en')
            if 'V-ie' in tags:
                additional.append('V-ie')
            if 'V-bi' in tags:
                additional.append('V-bi')
            if 'V-ey' in tags:
                additional.append('V-ey')
            if 'V-oy' in tags:
                additional.append('V-oy')
            if 'Coun' in tags:
                additional.append('Coun')
            if 'Af-p' in tags:
                additional.append('Af-p')
            if 'Anph' in tags:
                additional.append('Anph')
            if 'Subx' in tags:
                additional.append('Subx')
            if 'Vpre' in tags:
                additional.append('Vpre')
            if 'Prdx' in tags:
                additional.append('Prdx')
            if 'Coll' in tags:
                additional.append('Coll')
            if 'Adjx' in tags:
                additional.append('Adjx')
            if 'Qual' in tags:
                additional.append('Qual')
            if 'Apro' in tags:
                additional.append('Apro')
            if 'Anum' in tags:
                additional.append('Anum')
            if 'Poss' in tags:
                additional.append('Poss')
            if 'ms-f' in tags:
                additional.append('ms-f')
            if 'Ms-f' in tags:
                additional.append('Ms-f')
            if 'Impe' in tags:
                additional.append('Impe')
            if 'Impx' in tags:
                additional.append('Impx')
            if 'Mult' in tags:
                additional.append('Mult')
            if 'Abbr' in tags:
                additional.append('Abbr')
            if 'Fixd' in tags:
                additional.append('Fixd')

            gramma = Gramma(
                word,
                lemma,
                pos,
                gender,
                animacy,
                number,
                case,
                aspect,
                mood,
                person,
                poss,
                reflex,
                tense,
                verbForm,
                voice,
                degree,
                nameType,
                trans,
                invl,
                additional
            )
            sentence.append(gramma)
    
    return sentences

def loadNKRYGrammasFromFile(filename):
    with open(filename, 'r') as NKRY:
        sentences = []
        sentence = []
        for line in NKRY:
            line = line.strip()
            if line == 'BEGIN':
                sentence = []
                continue
            elif line == 'END':
                sentences.append(sentence)
                continue
        
            word = None
            lemma = None
            pos = None
            gender = None
            animacy = None
            number = None
            case = None
            aspect = None
            mood = None
            person = None
            poss = None
            reflex = None
            tense = None
            verbForm = None
            voice = None
            degree = None
            nameType = None
            trans = None
            invl = None
            fullForm = None
            additional = []

            lineParts = line.split('\t')
            word = lineParts[0]
            lemma = lineParts[1] if len(lineParts) > 1 else ""
            tags = lineParts[2] if len(lineParts) > 2 else ""
            tags = tags.split(",")
            pos = tags[0] if len(tags) else None
            tags = tags[1:] if len(tags) > 1 else []

            if 'm' in tags:
                gender = 'm'
            if 'f' in tags:
                gender = 'f'
            if 'n' in tags:
                gender = 'n'
            if 'm-f' in tags:
                gender = 'm-f'

            if 'anim' in tags:
                animacy = 'anim'
            if 'inan' in tags:
                animacy = 'inan'

            if 'sg' in tags:
                number = 'sg'
            if 'pl' in tags:
                number = 'pl'

            if 'nom' in tags:
                case = 'nom'
            if 'voc' in tags:
                case = 'voc'
            if 'gen' in tags:
                case = 'gen'
            if 'gen2' in tags:
                case = 'gen2'
            if 'adnum' in tags:
                case = 'adnum'
            if 'dat' in tags:
                case = 'dat'
            if 'dat2' in tags:
                case = 'dat2'
            if 'acc' in tags:
                case = 'acc'
            if 'acc2' in tags:
                case = 'acc2'
            if 'loc' in tags:
                case = 'loc'
            if 'loc2' in tags:
                case = 'loc2'
            if 'ins' in tags:
                case = 'ins'

            if 'brev' in tags:
                fullForm = 'brev'
            if 'plen' in tags:
                fullForm = 'plen'

            if 'ipf' in tags:
                aspect = 'ipf'
            if 'pf' in tags:
                aspect = 'pf'

            if 'indic' in tags:
                mood = 'indic'
            if 'imper' in tags:
                mood = 'imper'
            if 'imper2' in tags:
                mood = 'imper2'

            if '1p' in tags:
                person = '1p'
            if '2p' in tags:
                person = '2p'
            if '3p' in tags:
                person = '3p'
                
            if 'praet' in tags:
                tense = 'praet'
            if 'praes' in tags:
                tense = 'praes'
            if 'fut' in tags:
                tense = 'fut'

            if 'inf' in tags:
                verbForm = 'inf'
            if 'partcp' in tags:
                verbForm = 'partcp'
            if 'ger' in tags:
                verbForm = 'ger'

            if 'act' in tags:
                voice = 'act'
            if 'med' in tags:
                voice = 'med'
            if 'pass' in tags:
                voice = 'pass'

            if 'comp' in tags:
                degree = 'comp'
            if 'comp2' in tags:
                degree = 'comp2'
            if 'supr' in tags:
                degree = 'supr'

            if 'patrn' in tags:
                nameType = 'patrn'
            if 'zoon' in tags:
                nameType = 'zoon'
            if 'persn' in tags:
                nameType = 'persn'
            if 'famn' in tags:
                nameType = 'famn'

            if 'tran' in tags:
                trans = 'tran'
            if 'intr' in tags:
                trans = 'intr'

            gramma = Gramma(
                word,
                lemma,
                pos,
                gender,
                animacy,
                number,
                case,
                aspect,
                mood,
                person,
                poss,
                reflex,
                tense,
                verbForm,
                voice,
                degree,
                nameType,
                trans,
                invl,
                additional,
                fullForm
            )
            sentence.append(gramma)
    return sentences

def loadUDGrammasFromFile(filename):
    with open(filename, 'r') as UD:
        sentences = []
        sentence = []
        for line in UD:
            line = line.strip()
            if line == 'BEGIN':
                sentence = []
                continue
            elif line == 'END':
                sentences.append(sentence)
                continue
            
            word = None
            lemma = None
            pos = None
            gender = None
            animacy = None
            number = None
            case = None
            aspect = None
            mood = None
            person = None
            poss = None
            reflex = None
            tense = None
            verbForm = None
            voice = None
            degree = None
            nameType = None
            trans = None
            invl = None
            additional = []

            lineParts = line.split('\t')
            word = lineParts[0]
            lemma = lineParts[1] if len(lineParts) > 1 else ""
            tags = lineParts[2] if len(lineParts) > 2 else ""
            tags = tags.split(",")
            pos = tags[0] if len(tags) else None
            tags = tags[1:] if len(tags) > 1 else []

            if 'Gender=Masc' in tags:
                gender = 'Gender=Masc'
            if 'Gender=Fem' in tags:
                gender = 'Gender=Fem'
            if 'Gender=Neut' in tags:
                gender = 'Gender=Neut'
            if 'Animacy=Anim' in tags:
                animacy = 'Animacy=Anim'
            if 'Animacy=Inan' in tags:
                animacy = 'Animacy=Inan'
            if 'Number=Sing' in tags:
                number = 'Number=Sing'
            if 'Number=Coll' in tags:
                number = 'Number=Coll'
            if 'Number=Plur' in tags:
                number = 'Number=Plur'
            if 'Number=Ptan' in tags:
                number = 'Number=Ptan'
            if 'Case=Nom' in tags:
                case = 'Case=Nom'
            if 'Case=Gen' in tags:
                case = 'Case=Gen'
            if 'Case=Dat' in tags:
                case = 'Case=Dat'
            if 'Case=Acc' in tags:
                case = 'Case=Acc'
            if 'Case=Loc' in tags:
                case = 'Case=Loc'
            if 'Case=Ins' in tags:
                case = 'Case=Ins'
            if 'Aspect=Imp' in tags:
                aspect = 'Aspect=Imp'
            if 'Aspect=Perf' in tags:
                aspect = 'Aspect=Perf'
            if 'Mood=Ind' in tags:
                mood = 'Mood=Ind'
            if 'Mood=Cnd' in tags:
                mood = 'Mood=Cnd'
            if 'Mood=Imp' in tags:
                mood = 'Mood=Imp'
            if 'Person=1' in tags:
                person = 'Person=1'
            if 'Person=2' in tags:
                person = 'Person=2'
            if 'Person=3' in tags:
                person = 'Person=3'
            if 'Poss=Yes' in tags:
                poss = 'Poss=Yes'
            if 'Reflex=Yes' in tags:
                reflex = 'Reflex=Yes'
            if 'Tense=Past' in tags:
                tense = 'Tense=Past'
            if 'Tense=Pres' in tags:
                tense = 'Tense=Pres'
            if 'Tense=Fut' in tags:
                tense = 'Tense=Fut'
            if 'VerbForm=Fin' in tags:
                verbForm = 'VerbForm=Fin'
            if 'VerbForm=Inf' in tags:
                verbForm = 'VerbForm=Inf'
            if 'VerbForm=Part' in tags:
                verbForm = 'VerbForm=Part'
            if 'VerbForm=Trans' in tags:
                verbForm = 'VerbForm=Trans'
            if 'Voice=Act' in tags:
                voice = 'Voice=Act'
            if 'Voice=Mid' in tags:
                voice = 'Voice=Mid'
            if 'Voice=Pass' in tags:
                voice = 'Voice=Pass'
            if 'Degree=Pos' in tags:
                degree = 'Degree=Pos'
            if 'Degree=Cmp' in tags:
                degree = 'Degree=Cmp'
            if 'Degree=Sup' in tags:
                degree = 'Degree=Sup'
            if 'NameType=Geo' in tags:
                nameType = 'NameType=Geo'
            if 'NameType=Prs' in tags:
                nameType = 'NameType=Prs'
            if 'NameType=Giv' in tags:
                nameType = 'NameType=Giv'
            if 'NameType=Sur' in tags:
                nameType = 'NameType=Sur'
            if 'NameType=Com' in tags:
                nameType = 'NameType=Com'
            if 'NameType=Pro' in tags:
                nameType = 'NameType=Pro'
            if 'NameType=Oth' in tags:
                nameType = 'NameType=Oth'

            gramma = Gramma(
                word,
                lemma,
                pos,
                gender,
                animacy,
                number,
                case,
                aspect,
                mood,
                person,
                poss,
                reflex,
                tense,
                verbForm,
                voice,
                degree,
                nameType,
                trans,
                invl,
                additional
            )
            sentence.append(gramma)
    return sentences

def loadGIKRYGrammasFromFile(filename):
    with open(filename, 'r') as GIKRY:
        sentences = []
        sentence = []
        for line in GIKRY:
            line = line.strip()
            if line == 'BEGIN':
                sentence = []
                continue
            elif line == 'END':
                sentences.append(sentence)
                continue
        
            word = None
            lemma = None
            pos = None
            gender = None
            animacy = None
            number = None
            case = None
            aspect = None
            mood = None
            person = None
            poss = None
            reflex = None
            tense = None
            verbForm = None
            voice = None
            degree = None
            nameType = None
            trans = None
            invl = None
            fullForm = None
            additional = []
            nounType = None
            additionalCase = None
            aspectual = None
            categoryOfAdjective = None
            syntaxType = None
            categoryOfNumeral = None
            formOfNumeral = None
            typeOfAdposition = None
            structureOfAdposition = None
            typeOfAnother = None

            lineParts = line.split('\t')
            word = lineParts[0]
            lemma = lineParts[1] if len(lineParts) > 1 else ""
            tags = lineParts[2] if len(lineParts) > 2 else ""
            tags = tags.split(',')
            pos = tags[0] if len(tags) else None
            tags = tags[1:] if len(tags) > 1 else []

            if pos == 'N':
                nounType = tags[0]
                gender = tags[1]
                number = tags[2]
                case = tags[3]
                additionalCase = tags[4]
                animacy = tags[5]
            if pos == 'A':
                degree = tags[0]
                gender = tags[1] if len(tags) >= 2 else None
                number = tags[2] if len(tags) >= 3 else None
                case = tags[3] if len(tags) >= 4 else None
                fullForm = tags[4] if len(tags) >= 5 else None
            if pos == 'V':
                if tags[0] in ['i', 'm']:
                    mood = tags[0]
                elif tags[0] in ['n', 'g', 'p', 'x']:
                    verbForm = tags[0]
                gender = tags[1]
                number = tags[2]
                case = tags[3] if len(tags) >= 4 else None
                person = tags[4] if len(tags) >= 5 else None
                tense = tags[5] if len(tags) >= 6 else None
                trans = tags[6] if len(tags) >= 7 else None
                voice = tags[7] if len(tags) >= 8 else None
                aspect = tags[8] if len(tags) >= 9 else None
                aspectual = tags[9] if len(tags) >= 10 else None
                fullForm = tags[10] if len(tags) >= 11 else None

            if pos == 'R':
                degree = tags[0]

            # if pos == 'W':

            if pos == 'P':
                categoryOfAdjective = tags[0]
                gender = tags[1] if len(tags) >= 2 else None
                number = tags[2] if len(tags) >= 3 else None
                case = tags[3] if len(tags) >= 4 else None
                person = tags[4] if len(tags) >= 5 else None
                syntaxType = tags[5] if len(tags) >= 6 else None

            if pos == 'M':
                categoryOfNumeral = tags[0] if len(tags) >= 1 else None
                gender = tags[1] if len(tags) >= 2 else None
                number = tags[2] if len(tags) >= 3 else None
                case = tags[3] if len(tags) >= 4 else None
                formOfNumeral = tags[4] if len(tags) >= 5 else None

            if pos == 'S':
                typeOfAdposition = tags[0]
                structureOfAdposition = tags[1]
                case = tags[3] if len(tags) >= 4 else None
            # if pos == 'C':

            # if pos == 'H':

            # if pos == 'I':

            # if pos == 'Q':

            if pos == 'X':
                typeOfAnother = tags[0] if len(tags) > 0 else None
            gramma = Gramma(
                word,
                lemma,
                pos,
                gender,
                animacy,
                number,
                case,
                aspect,
                mood,
                person,
                poss,
                reflex,
                tense,
                verbForm,
                voice,
                degree,
                nameType,
                trans,
                invl,
                additional,
                fullForm,
                nounType,
                additionalCase,
                aspectual,
                categoryOfAdjective,
                syntaxType,
                categoryOfNumeral,
                formOfNumeral,
                typeOfAdposition,
                structureOfAdposition,
                typeOfAnother
            )
            sentence.append(gramma)
    return sentences