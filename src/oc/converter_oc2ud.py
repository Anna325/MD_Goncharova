from src.common.gramma import Gramma
from src.ud.predictor import UDPredictor
import sys

class OC2UDConverter():
    def __init__(self, use_prediction):
        self.posPredictor = UDPredictor('pos')
        self.moodPredictor = UDPredictor('mood')
        self.voicePredictor = UDPredictor('voice')
        self.nameTypePredictor = UDPredictor('nameType')
        self.possPredictor = UDPredictor('poss')
        self.reflexPredictor = UDPredictor('reflex')
        self.degreePredictor = UDPredictor('degree')
        self.use_prediction = use_prediction

    def convert(self, oc_sentences):
        ud_sentences = []
        for sentence_index in range(len(oc_sentences)):
            oc_sentence = oc_sentences[sentence_index]
            sys.stdout.write("convert %s/%s\r" % (sentence_index, len(oc_sentences)))
            sys.stdout.flush()
            ud_sentence = []
            for index in range(len(oc_sentence)):
                oc_gramma = oc_sentence[index]
                ud_gramma = self.convertGramma(oc_gramma, oc_sentence, index)
                ud_sentence.append(ud_gramma)
            ud_sentences.append(ud_sentence)
        
        return ud_sentences

    def convertGramma(self, oc_gramma, sentence, grammaInSentenceIndex):
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

        # Ошибок больше, чем через модель
        # if oc_gramma.pos == 'NOUN': pos = 'NOUN'
        # if oc_gramma.pos == 'NOUN' and (
        #                         oc_gramma.nameType == 'Name' or
        #                         oc_gramma.nameType == 'Surn' or
        #                         oc_gramma.nameType == 'Patr' or
        #                         oc_gramma.nameType == 'Geox' or
        #                         oc_gramma.nameType == 'Orgn' or
        #                         oc_gramma.nameType == 'Trad' or
        #                         oc_gramma.nameType == 'Init'): pos = 'PROPN'
        if oc_gramma.pos == 'NOUN': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['NOUN', 'PROPN'])
        if oc_gramma.pos == 'NPRO': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['PRON', 'DET'])
        if oc_gramma.pos == 'ADJF': pos = 'ADJ'
        if oc_gramma.pos == 'ADJS': pos = 'ADJ'
        if oc_gramma.pos == 'COMP': pos = 'ADJ'
        if oc_gramma.pos == 'NUMR': pos = 'NUM'
        if oc_gramma.pos == 'ADVB': pos = 'ADV'
        if oc_gramma.pos == 'PRED': pos = 'ADV'
        if oc_gramma.pos == 'VERB': pos = 'VERB'
        if oc_gramma.pos == 'INFN': 
            verbForm = 'VerbForm=Inf'
            pos = 'VERB'
        if oc_gramma.pos == 'PRTF': 
            verbForm = 'VerbForm=Part'
            pos = 'VERB'
        if oc_gramma.pos == 'PRTS': 
            verbForm = 'VerbForm=Part'
            pos = 'VERB'
        if oc_gramma.pos == 'GRND': 
            verbForm = 'VerbForm=Trans'
            pos = 'VERB'
        if oc_gramma.pos == 'CONJ': pos = 'CONJ'
        if oc_gramma.pos == 'PREP': pos = 'ADP'
        if oc_gramma.pos == 'INTJ': pos = 'INTJ'
        if oc_gramma.pos == 'PRCL': pos = 'PART'
        if oc_gramma.pos == 'PNCT': pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['PUNCT', 'SYM'])
        if oc_gramma.pos == 'LATN': pos = 'X'
        if oc_gramma.pos == 'NUMB': pos = 'X'
        if oc_gramma.pos == 'ROMN': pos = 'X'
        if oc_gramma.pos == 'UNKN': pos = 'X'

        if oc_gramma.gender == 'masc': gender = 'Gender=Masc'
        if oc_gramma.gender == 'femn': gender = 'Gender=Fem'
        if oc_gramma.gender == 'neut': gender = 'Gender=Neut'
        
        if oc_gramma.animacy == 'anim': animacy = 'Animacy=Anim'
        if oc_gramma.animacy == 'inan': animacy = 'Animacy=Inan'
        
        if oc_gramma.number == 'sing': number = 'Number=Sing'
        if oc_gramma.number == 'plur': number = 'Number=Plur'
        if oc_gramma.number == 'Pltm': number = 'Number=Ptan'
        if oc_gramma.number == 'Sgtm': number = 'Number=Coll'
        
        if oc_gramma.case == 'nomn' or oc_gramma.case == 'voct': case = 'Case=Nom'
        if oc_gramma.case == 'gent' or oc_gramma.case =='gen1' or oc_gramma.case =='gen2': case = 'Case=Gen'
        if oc_gramma.case == 'datv': case = 'Case=Dat'
        if oc_gramma.case == 'accs' or oc_gramma.case =='acc2': case = 'Case=Acc'
        if oc_gramma.case == 'loct' or oc_gramma.case =='loc1' or oc_gramma.case =='loc2': case = 'Case=Loc'
        if oc_gramma.case == 'ablt': case = 'Case=Ins'
        
        if oc_gramma.aspect == 'impf': aspect = 'Aspect=Imp'
        if oc_gramma.aspect == 'perf': aspect = 'Aspect=Perf'
        
        if oc_gramma.verbForm == 'INFN':
            verbForm = 'VerbForm=Inf'
        if oc_gramma.verbForm == 'PRTF':
            verbForm = 'VerbForm=Part'
        if oc_gramma.verbForm == 'PRTS':
            verbForm = 'VerbForm=Part'
        if oc_gramma.verbForm == 'GRND':
            verbForm = 'VerbForm=Trans'
        # попробовать модель для остальных случаев

        if oc_gramma.mood == 'indc':
            verbForm = 'VerbForm=Fin'
            mood = self.predict(self.moodPredictor, sentence, grammaInSentenceIndex, ['Mood=Ind', 'Mood=Cnd'])
        if oc_gramma.mood == 'impr':
            verbForm = 'VerbForm=Fin'
            mood = 'Mood=Imp'
        
        if oc_gramma.person == '1per': person = 'Person=1'
        if oc_gramma.person == '2per': person = 'Person=2'
        if oc_gramma.person == '3per': person = 'Person=3'

        if oc_gramma.tense == 'past': tense = 'Tense=Past'
        if oc_gramma.tense == 'pres': tense = 'Tense=Pres'
        if oc_gramma.tense == 'futr': tense = 'Tense=Fut'

        if oc_gramma.voice == 'actv': voice = self.predict(self.voicePredictor, sentence, grammaInSentenceIndex, ['Voice=Act', 'Voice=Mid'])
        if oc_gramma.voice == 'pssv': voice = 'Voice=Pass'

        if oc_gramma.nameType == 'Geox': nameType = 'NameType=Geo'
        if oc_gramma.nameType == 'Patr': nameType = 'NameType=Prs'
        if oc_gramma.nameType == 'Name': nameType = self.predict(self.nameTypePredictor, sentence, grammaInSentenceIndex, ['NameType=Prs', 'NameType=Giv'])
        if oc_gramma.nameType == 'Surn': nameType = 'NameType=Sur'
        if oc_gramma.nameType == 'Orgn': nameType = 'NameType=Com'
        if oc_gramma.nameType == 'Trad': nameType = 'NameType=Pro'
        if oc_gramma.nameType == 'Init': nameType = 'NameType=Oth'

        degree = self.predict(self.degreePredictor, sentence, grammaInSentenceIndex, [None, 'Degree=Pos', 'Degree=Cmp', 'Degree=Sup'])
        poss = self.predict(self.possPredictor, sentence, grammaInSentenceIndex, [None, 'Poss=Yes'])
        reflex = self.predict(self.reflexPredictor, sentence, grammaInSentenceIndex, [None, 'Reflex=Yes'])

        gramma = Gramma(
            oc_gramma.word,
            oc_gramma.lemma,
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