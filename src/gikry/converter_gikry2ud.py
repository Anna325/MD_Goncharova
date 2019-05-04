from src.common.gramma import Gramma
from src.ud.predictor import UDPredictor
import sys

class GIKRY2UDConverter():
    def __init__(self, use_prediction):
        self.posPredictor = UDPredictor('pos')
        self.numberPredictor = UDPredictor('number')
        self.possPredictor = UDPredictor('poss')
        self.reflexPredictor = UDPredictor('reflex')
        self.moodPredictor = UDPredictor('mood')
        self.verbFormPredictor = UDPredictor('verbForm')
        self.nameTypePredictor = UDPredictor('nameType')
        self.use_prediction = use_prediction

    def convert(self, gikry_sentences):
        ud_sentences = []
        for index in range(len(gikry_sentences)):
            sys.stdout.write("convery %s/%s\r" % (index, len(gikry_sentences)))
            sys.stdout.flush()
            gikry_sentence = gikry_sentences[index]
            ud_sentence = []
            for grammaIndex in range(len(gikry_sentence)):
                gikry_gramma = gikry_sentence[grammaIndex]
                ud_gramma = self.convertGramma(gikry_gramma, gikry_sentence, grammaIndex)
                ud_sentence.append(ud_gramma)
            ud_sentences.append(ud_sentence)

        return ud_sentences
    
    def convertGramma(self, gikry_gramma, sentence, grammaInSentenceIndex):
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

        if gikry_gramma.pos == 'N':
            pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['NOUN', 'PROPN'])
        if gikry_gramma.pos == 'P':
            pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['PRON', 'DET'])
        if gikry_gramma.pos == 'A':
            pos = 'ADJ'
        if gikry_gramma.pos == 'M':
            pos = 'NUM'
        if gikry_gramma.pos == 'R':
            pos = 'ADV'
        if gikry_gramma.pos == 'W':
            pos = 'ADV'
        if gikry_gramma.pos == 'V':
            pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['VERB', 'AUX'])
        if gikry_gramma.pos == 'C':
            pos = 'CONJ'
        if gikry_gramma.pos == 'S':
            pos = 'ADP'
        if gikry_gramma.pos == 'I':
            pos = 'INTJ'
        if gikry_gramma.pos == 'H':
            pos = 'X'
        if gikry_gramma.pos == 'Q':
            pos = "PART"
        if gikry_gramma.pos == 'X':
            pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['SYM', 'PUNCT', 'X'])

        if gikry_gramma.gender == 'm':
            gender = 'Gender=Masc'
        elif gikry_gramma.gender == 'f':
            gender = 'Gender=Fem'
        elif gikry_gramma.gender == 'n':
            gender = 'Gender=Neut'

        if gikry_gramma.animacy == 'y':
            animacy = 'Animacy=Anim'
        if gikry_gramma.animacy == 'n':
            animacy = 'Animacy=Inan'

        if gikry_gramma.number == 's':
            number = 'Number=Sing'
        if gikry_gramma.number == 'p':
            number = 'Number=Plur'
        if gikry_gramma.number == 'i':
            number = self.predict(self.numberPredictor, sentence, grammaInSentenceIndex, ['Number=Ptan', 'Number=Coll'])

        if gikry_gramma.case == 'n' or gikry_gramma.case == 'v':
            case = 'Case=Nom'
        if gikry_gramma.case == 'g' or gikry_gramma.case == 'p':
            case = 'Case=Gen'
        if gikry_gramma.case == 'd':
            case = 'Case=Dat'
        if gikry_gramma.case == 'a':
            case = 'Case=Acc'
        if gikry_gramma.case == 'l':
            case = 'Case=Loc'
        if gikry_gramma.case == 'i':
            case = 'Case=Ins'

        if gikry_gramma.aspect == 'i':
            aspect = 'Aspect=Imp'
        if gikry_gramma.aspect == 'p':
            aspect = 'Aspect=Perf'

        if gikry_gramma.mood == 'i':
            mood = self.predict(self.moodPredictor, sentence, grammaInSentenceIndex, ['Mood=Ind', 'Mood=Cnd'])
        if gikry_gramma.mood == 'm':
            mood = 'Mood=Imp'

        if gikry_gramma.person == '1':
            person = 'Person=1'
        if gikry_gramma.person == '2':
            person = 'Person=2'
        if gikry_gramma.person == '3':
            person = 'Person=3'

        poss = self.predict(self.possPredictor, sentence, grammaInSentenceIndex, [None, 'Poss=Yes'])
        poss = self.predict(self.reflexPredictor, sentence, grammaInSentenceIndex, [None, 'Reflex=Yes'])

        if gikry_gramma.tense == 's':
            tense = 'Tense=Past'
        if gikry_gramma.tense == 'p':
            tense = 'Tense=Pres'
        if gikry_gramma.tense == 'f':
            tense = 'Tense=Fut'

        if gikry_gramma.verbForm == 'n':
            verbForm = 'VerbForm=Inf'
        elif gikry_gramma.verbForm == 'p':
            verbForm = 'VerbForm=Part'
        elif gikry_gramma.verbForm == 'g':
            verbForm = 'VerbForm=Trans'
        # else:
            # verbForm = self.predict(self.verbFormPredictor, sentence, grammaInSentenceIndex, [None, 'VerbForm=Fin'])

        if gikry_gramma.voice == 'a':
            voice = 'Voice=Act'
        if gikry_gramma.voice == 'p':
            voice = 'Voice=Mid'
        if gikry_gramma.voice == 's':
            voice = 'Voice=Pass'

        if gikry_gramma.degree == 'p':
            degree = 'Degree=Pos'
        if gikry_gramma.degree == 'c':
            degree = 'Degree=Cmp'
        if gikry_gramma.degree == 's':
            degree = 'Degree=Sup'

        nameType = self.predict(
            self.nameTypePredictor, 
            sentence, 
            grammaInSentenceIndex, 
            [
                None,
                'NameType=Geo',
                'NameType=Prs',
                'NameType=Giv',
                'NameType=Sur',
                'NameType=Com',
                'NameType=Pro',
                'NameType=Oth',
            ]
        )
     
        gramma = Gramma(
            gikry_gramma.word,
            gikry_gramma.lemma,
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
