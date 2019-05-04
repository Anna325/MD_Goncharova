from src.common.gramma import Gramma
from src.nkry.predictor import NKRYPrecitor
import sys

class UD2NKRYConverter():
    def __init__(self, use_prediction):
        self.posPredictor = NKRYPrecitor('pos')
        self.casePredictor = NKRYPrecitor('case')
        self.moodPredictor = NKRYPrecitor('mood')
        self.degreePredictor = NKRYPrecitor('degree')
        self.nameTypePredictor = NKRYPrecitor('nameType')
        self.transPredictor = NKRYPrecitor('trans')
        self.fullFormPredictor = NKRYPrecitor('fullForm')
    
        self.use_prediction = use_prediction

    def convert(self, ud_sentences):
        nkry_sentences = []
        for index in range(len(ud_sentences)):
            sys.stdout.write("convert %s/%s\r" % (index, len(ud_sentences)))
            sys.stdout.flush()
            ud_sentence = ud_sentences[index]
            nkry_sentence = []
            for grammaIndex in range(len(ud_sentence)):
                ud_gramma = ud_sentence[grammaIndex]
                nkry_gramma = self.convertGramma(ud_gramma, ud_sentence, grammaIndex)
                nkry_sentence.append(nkry_gramma)
            nkry_sentences.append(nkry_sentence)
        
        return nkry_sentences

    def convertGramma(self, ud_gramma, sentence, grammaInSentenceIndex):
        pos = '-'
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
        fullForm = None

        if ud_gramma.gender == 'Gender=Masc': gender = 'm'
        if ud_gramma.gender == 'Gender=Fem': gender = 'f'
        if ud_gramma.gender == 'Gender=Neut': gender = 'n'
        # todo - сделать угадывание пола m-f

        if ud_gramma.animacy == 'Animacy=Anim': animacy = 'anim'
        if ud_gramma.animacy == 'Animacy=Inan': animacy = 'inan'
            
        if ud_gramma.number == 'Number=Sing': number = 'sg'
        if ud_gramma.number == 'Number=Plur': number = 'pl'
        if ud_gramma.number == 'Number=Ptan': number = 'pl'
        if ud_gramma.number == 'Number=Coll': number = 'sg'

        if ud_gramma.case == 'Case=Nom': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['nom', 'voc'])
        if ud_gramma.case == 'Case=Gen': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['gen', 'gen2', 'adnum'])
        if ud_gramma.case == 'Case=Dat': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['dat', 'dat2'])
        if ud_gramma.case == 'Case=Acc': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['acc', 'acc2'])
        if ud_gramma.case == 'Case=Loc': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['loc', 'loc2'])
        if ud_gramma.case == 'Case=Ins': case = 'ins'

        fullForm = self.predict(self.fullFormPredictor, sentence, grammaInSentenceIndex, [None, 'brev', 'plen'])        


        if ud_gramma.aspect == 'Aspect=Imp': aspect = 'ipf'
        if ud_gramma.aspect == 'Aspect=Perf': aspect = 'pf'
        if ud_gramma.mood == 'Mood=Ind': mood = 'indic'
        if ud_gramma.mood == 'Mood=Cnd': mood = 'indic'
        if ud_gramma.mood == 'Mood=Imp': mood = 'imper'
            # todo - сделать угадывание mood=imper2

        if ud_gramma.person == 'Person=1': person = '1p'
        if ud_gramma.person == 'Person=2': person = '2p'
        if ud_gramma.person == 'Person=3': person = '3p'

        if ud_gramma.tense == 'Tense=Past': tense = 'praet'
        if ud_gramma.tense == 'Tense=Pres': tense = 'praes'
        if ud_gramma.tense == 'Tense=Fut': tense = 'fut'

        if ud_gramma.verbForm == 'VerbForm=Fin': verbForm = None
        if ud_gramma.verbForm == 'VerbForm=Inf': verbForm = 'inf'
        if ud_gramma.verbForm == 'VerbForm=Part': verbForm = 'partcp'
        if ud_gramma.verbForm == 'VerbForm=Trans': verbForm = 'ger'

        if ud_gramma.voice == 'Voice=Act': voice = 'act'
        if ud_gramma.voice == 'Voice=Mid': voice = 'med'
        if ud_gramma.voice == 'Voice=Pass': voice = 'pass'

        if ud_gramma.degree == 'Degree=Pos': degree = None
        if ud_gramma.degree == 'Degree=Cmp': degree = self.predict(self.degreePredictor, sentence, grammaInSentenceIndex, ['comp', 'comp2'])
        if ud_gramma.degree == 'Degree=Sup': degree = 'supr'
            
        if ud_gramma.nameType == 'NameType=Geo': nameType = None
        if ud_gramma.nameType == 'NameType=Prs': nameType = 'patrn'
        if ud_gramma.nameType == 'NameType=Giv': nameType = self.predict(self.nameTypePredictor, sentence, grammaInSentenceIndex, ['zoon', 'persn'])
        if ud_gramma.nameType == 'NameType=Sur': nameType = 'famn'
        if ud_gramma.nameType == 'NameType=Com': nameType = None
        if ud_gramma.nameType == 'NameType=Pro': nameType = None
        if ud_gramma.nameType == 'NameType=Oth': nameType = None
        trans = self.predict(self.transPredictor, sentence, grammaInSentenceIndex, [None, 'tran', 'intr'])

        if ud_gramma.pos == 'NOUN': pos = 'S'
        if ud_gramma.pos == 'PROPN': pos = 'S'
        if ud_gramma.pos == 'PRON': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['SPRO', 'PREADICPRO'])
        if ud_gramma.pos == 'DET': pos = 'APRO'
        if ud_gramma.pos == 'ADJ': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['A', 'ANUM'])
        if ud_gramma.pos == 'NUM': pos = 'NUM'
        if ud_gramma.pos == 'CONJ': 
            if ud_gramma.word == 'где' or ud_gramma.word == 'вот':
                pos = 'ADVPRO'
            else:
                pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['CONJ', 'ADVPRO', 'PARENTH'])

        if ud_gramma.pos == 'ADV': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['ADV', 'PRAEDIC'])
        if ud_gramma.pos == 'PART': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['PART', 'ADVPRO'])
        if ud_gramma.pos == 'ADP': pos = 'PR'
        if ud_gramma.pos == 'AUX': pos = 'V'
        if ud_gramma.pos == 'VERB': pos = 'V'
        if ud_gramma.pos == 'INTJ': pos = 'INTJ'
        if ud_gramma.pos == 'PART': pos = 'PART'
        if ud_gramma.pos == 'SYM': pos = '-'
        if ud_gramma.pos == 'PUNCT': pos = '-'
        if ud_gramma.pos == 'X': pos = '-'


        gramma = Gramma(
            ud_gramma.word,
            ud_gramma.lemma,
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
        
        return gramma

    def predict(self, predictor, sentence, grammaInSentenceIndex, variants, debug=False):
        if not self.use_prediction:
            return variants[0]
        prediction = predictor.predict(sentence, grammaInSentenceIndex)
        if debug == True:
            print("Prediction is: %s" % prediction)
        if not prediction or prediction not in variants:
            return variants[0]
        else:
            return prediction