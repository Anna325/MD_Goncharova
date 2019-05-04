from src.common.gramma import Gramma
from src.ud.predictor import UDPredictor
import sys

class NKRY2UDConverter():
    def __init__(self, use_prediction):
        self.posPredictor = UDPredictor('pos')
        self.moodPredictor = UDPredictor('mood')
        self.voicePredictor = UDPredictor('voice')
        self.nameTypePredictor = UDPredictor('nameType')
        self.possPredictor = UDPredictor('poss')
        self.reflexPredictor = UDPredictor('reflex')
        self.degreePredictor = UDPredictor('degree')
        self.genderPredictor = UDPredictor('gender')
        self.casePredictor = UDPredictor('case')
        self.verbFormPredictor = UDPredictor('verbForm')
        self.numberPredictor = UDPredictor('number')
        self.use_prediction = use_prediction

    def convert(self, nkry_sentences):
        ud_sentences = []
        for index in range(len(nkry_sentences)):
            sys.stdout.write("convert %s/%s\r" % (index, len(nkry_sentences)))
            sys.stdout.flush()
            nkry_sentence = nkry_sentences[index]
            ud_sentence = []
            for grammaIndex in range(len(nkry_sentence)):
                nkry_gramma = nkry_sentence[grammaIndex]
                ud_gramma = self.convertGramma(nkry_gramma, nkry_sentence, grammaIndex)
                ud_sentence.append(ud_gramma)
            ud_sentences.append(ud_sentence)
        
        return ud_sentences

    def convertGramma(self, nkry_gramma, sentence, grammaInSentenceIndex):
        pos = 'X'
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

        if nkry_gramma.pos == 'S': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['NOUN', 'PROPN'])
        elif nkry_gramma.pos == 'SPRO' or nkry_gramma.pos == 'PRAEDICPRO': pos = 'PRON'
        elif nkry_gramma.pos == 'APRO': pos = 'DET'
        elif nkry_gramma.pos == 'A' or nkry_gramma.pos == 'ANUM': pos = 'ADJ'
        elif nkry_gramma.pos == 'NUM': pos = 'NUM'
        elif nkry_gramma.pos == 'ADVPRO' and nkry_gramma.word == 'где': pos = 'CONJ'
        elif nkry_gramma.pos == 'ADVPRO' and nkry_gramma.word == 'вот': pos = 'PART'
        elif nkry_gramma.pos == 'ADV' or nkry_gramma.pos == 'PRAEDIC': pos = 'ADV'
        elif nkry_gramma.pos == 'PARENTH' and nkry_gramma.word == 'кстати': pos = 'CONJ'
        elif nkry_gramma.pos == 'PARENTH' and nkry_gramma.word == 'по-моему': pos = 'ADP'
        elif nkry_gramma.pos == 'V': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['VERB', 'V'])
        elif nkry_gramma.pos == 'CONJ': pos = 'CONJ'
        elif nkry_gramma.pos == 'PR': pos = 'ADP'
        elif nkry_gramma.pos == 'INTJ': pos = 'INTJ'
        elif nkry_gramma.pos == 'PART': pos = 'PART'
        else: pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['SYM', 'PUNCT', 'X'])

        if nkry_gramma.gender == 'm': gender = 'Gender=Masc'
        if nkry_gramma.gender == 'f': gender = 'Gender=Fem'
        if nkry_gramma.gender == 'n': gender = 'Gender=Neut'
        if nkry_gramma.gender == 'm-f': gender = self.predict(self.genderPredictor, sentence, grammaInSentenceIndex, [None, 'Gender=Masc', 'Gender=Fem', 'Gender=Neut'])
        
        if nkry_gramma.animacy == 'anim': animacy = 'Animacy=Anim'
        if nkry_gramma.animacy == 'inan': animacy = 'Animacy=Inan'

        if nkry_gramma.number == 'sg': number = self.predict(self.numberPredictor, sentence, grammaInSentenceIndex, ['Number=Sing', 'Number=Coll'])
        if nkry_gramma.number == 'pl': number = self.predict(self.numberPredictor, sentence, grammaInSentenceIndex, ['Number=Plur', 'Number=Ptan'])

        if nkry_gramma.case == 'nom' or nkry_gramma.case == 'voc': case = "Case=Nom"
        if nkry_gramma.case == 'gen' or nkry_gramma.case == 'gen2' or nkry_gramma.case == 'adnum': case = "Case=Gen"
        if nkry_gramma.case == 'dat' or nkry_gramma.case == 'dat2': case = "Case=Dat"
        if nkry_gramma.case == 'acc' or nkry_gramma.case == 'acc2': case = "Case=Acc"
        if nkry_gramma.case == 'loc' or nkry_gramma.case == 'loc2': case = "Case=Loc"
        if nkry_gramma.case == 'ins': case = "Case=Ins"
        if nkry_gramma.case == 'brev' or nkry_gramma.case == 'plen': 
            case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, [
                'Case=Nom',
                'Case=Gen',
                'Case=Dat',
                'Case=Acc',
                'Case=Loc',
                'Case=Ins',
            ])
            
        if nkry_gramma.aspect == 'ipf': aspect = 'Aspect=Imp'
        if nkry_gramma.aspect == 'pf': aspect = 'Aspect=Perf'
        
        if nkry_gramma.mood == 'indic': mood = self.predict(self.moodPredictor, sentence, grammaInSentenceIndex, ['Mood=Ind', 'Mood=Cnd'])
        if nkry_gramma.mood == 'imper': mood = 'Mood=Imp'
        if nkry_gramma.mood == 'imper2': mood = self.predict(self.moodPredictor, sentence, grammaInSentenceIndex, [None, 'Mood=Ind', 'Mood=Cnd', 'Mood=Imp'])

        if nkry_gramma.person == '1p': person = "Person=1"
        if nkry_gramma.person == '2p': person = "Person=2"
        if nkry_gramma.person == '3p': person = "Person=3"

        poss = self.predict(self.possPredictor, sentence, grammaInSentenceIndex, [None, 'Poss=Yes'])
        reflex = self.predict(self.reflexPredictor, sentence, grammaInSentenceIndex, [None, 'Reflex=Yes'])

        if nkry_gramma.tense == 'praet': tense = "Tense=Past"
        if nkry_gramma.tense == 'praes': tense = "Tense=Pres"
        if nkry_gramma.tense == 'fut': tense = "Tense=Fut"

        if nkry_gramma.verbForm == 'inf': verbForm = "VerbForm=Inf"
        elif nkry_gramma.verbForm == 'partcp': verbForm = "VerbForm=Part"
        elif nkry_gramma.verbForm == 'ger': verbForm = "VerbForm=Trans"
        else: verbForm = self.predict(self.verbFormPredictor, sentence, grammaInSentenceIndex, [None, 'VerbForm=Fin'])

        if nkry_gramma.voice == 'act': voice = 'Voice=Act'
        if nkry_gramma.voice == 'med': voice = 'Voice=Mid'
        if nkry_gramma.voice == 'pass': voice = 'Voice=Pass'

        if nkry_gramma.degree == 'comp' or nkry_gramma.degree == 'comp2': degree = "Degree=Cmp"
        elif nkry_gramma.degree == 'supr': degree = "Degree=Sup"
        else: degree = self.predict(self.degreePredictor, sentence, grammaInSentenceIndex, [None, 'Degree=Pos'])
        
        if nkry_gramma.nameType == 'patrn': nameType = 'NameType=Prs'
        elif nkry_gramma.nameType == 'zoon' or nkry_gramma.nameType == 'persn': nameType = 'NameType=Giv'
        elif nkry_gramma.nameType == 'famn': nameType = 'NameType=Sur'
        else: nameType = self.predict(self.nameTypePredictor, sentence, grammaInSentenceIndex, [
            None,
            'NameType=Geo'
            'NameType=Com'
            'NameType=Pro'
            'NameType=Oth'
        ])

        gramma = Gramma(
            nkry_gramma.word,
            nkry_gramma.lemma,
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
        
        return gramma
    
    def predict(self, predictor, sentence, grammaInSentenceIndex, variants):
        if not self.use_prediction:
            return variants[0]
        prediction = predictor.predict(sentence, grammaInSentenceIndex)
        if not prediction or prediction not in variants:
            return variants[0]
        else:
            return prediction