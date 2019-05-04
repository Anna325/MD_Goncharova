from src.common.gramma import Gramma
from src.gikry.predictor import GIKRYPredictor
import sys

class UD2GIKRYConverter():
    def __init__(self, use_prediction):
        self.posPredictor = GIKRYPredictor('pos')
        self.genderPredictor = GIKRYPredictor('gender')
        self.casePredictor = GIKRYPredictor('case')
        self.nounTypePredictor = GIKRYPredictor('nounType')
        self.fullFormPredictor = GIKRYPredictor('fullForm')
        self.aspectPredictor = GIKRYPredictor('aspect')
        self.aspectualPredictor = GIKRYPredictor('aspectual')
        self.tensePredictor = GIKRYPredictor('tense')
        self.verbFormPredictor = GIKRYPredictor('verbForm')
        self.transPredictor = GIKRYPredictor('trans')
        self.categoryOfAdjectivePredictor = GIKRYPredictor('categoryOfAdjective')
        self.syntaxTypePredictor = GIKRYPredictor('syntaxType')
        self.typeOfAnotherPredictor = GIKRYPredictor('typeOfAnother')
        self.typeOfAdpositionPredictor = GIKRYPredictor('typeOfAdposition')
        self.structureOfAdpositionPredictor = GIKRYPredictor('structureOfAdposition')
        self.categoryOfNumeralPredictor = GIKRYPredictor('categoryOfNumeral')
        self.formOfNumeralPredictor = GIKRYPredictor('formOfNumeral')
        self.use_prediction = use_prediction

    def convert(self, ud_sentences):
        gikry_sentences = []
        for index in range(len(ud_sentences)):
            sys.stdout.write("convert %s/%s\r" % (index, len(ud_sentences)))
            sys.stdout.flush()
            ud_sentence = ud_sentences[index]
            gikry_sentence = []
            for grammaIndex in range(len(ud_sentence)):
                ud_gramma = ud_sentence[grammaIndex]
                gikry_gramma = self.convertGramma(ud_gramma, ud_sentence, grammaIndex)
                gikry_sentence.append(gikry_gramma)
            gikry_sentences.append(gikry_sentence)

        return gikry_sentences
    
    def convertGramma(self, ud_gramma, sentence, grammaInSentenceIndex):
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
        fullForm = None
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

        if ud_gramma.pos == 'NOUN':
            pos = 'N'
        if ud_gramma.pos == 'PROPN':
            pos = 'N'
        if ud_gramma.pos == 'PRON':
            pos = 'P'
        if ud_gramma.pos == 'DET':
            pos = 'P'
        if ud_gramma.pos == 'ADJ':
            pos = 'A'
        if ud_gramma.pos == 'NUM':
            pos = 'M'
        if ud_gramma.pos == 'ADV':
            pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['R', 'W'])
        if ud_gramma.pos == 'AUX':
            pos = 'V'
        if ud_gramma.pos == 'VERB':
            pos = 'V'
        if ud_gramma.pos == 'CONJ':
            pos = 'C'
        if ud_gramma.pos == 'ADP':
            pos = 'S'
        if ud_gramma.pos == 'INTJ':
            pos = 'I'
        if ud_gramma.pos == 'PART':
            pos = 'Q'
        if ud_gramma.pos == 'SYM':
            pos = 'X'
        if ud_gramma.pos == 'PUNCT':
            pos = 'X'
        if ud_gramma.pos == 'X':
            pos = 'X'

        if ud_gramma.gender == 'Gender=Masc': gender = 'm'
        elif ud_gramma.gender == 'Gender=Fem': gender = 'f'
        elif ud_gramma.gender == 'Gender=Neut': gender = 'n'
        else:
            gender = self.predict(self.genderPredictor, sentence, grammaInSentenceIndex, [None, 'c'])
        
        if ud_gramma.animacy == 'Animacy=Anim': animacy = 'y'
        if ud_gramma.animacy == 'Animacy=Inan': animacy = 'n'

        if ud_gramma.number == 'Number=Sing': number = 's'
        if ud_gramma.number == 'Number=Plur': number = 'p'
        if ud_gramma.number == 'Number=Ptan': number = 'i'
        if ud_gramma.number == 'Number=Coll': number = 'i'

        if ud_gramma.case == 'Case=Nom': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['n', 'v'])
        if ud_gramma.case == 'Case=Gen': case = self.predict(self.casePredictor, sentence, grammaInSentenceIndex, ['g', 'p'])
        if ud_gramma.case == 'Case=Dat': case = 'd'
        if ud_gramma.case == 'Case=Acc': case = 'a'
        if ud_gramma.case == 'Case=Loc': case = 'l'
        if ud_gramma.case == 'Case=Ins': case = 'i'

        if pos == 'N':
            nounType = self.predict(self.nounTypePredictor, sentence, grammaInSentenceIndex, ['c', 'p'])
            
        if pos == 'A':
            fullForm = self.predict(self.fullFormPredictor, sentence, grammaInSentenceIndex, ['s', 'f'])

        if pos == 'V':
            if ud_gramma.aspect == 'Aspect=Imp': aspect = 'i'
            elif ud_gramma.aspect == 'Aspect=Perf': aspect = 'p'
            else:
                aspect = self.predict(self.aspectPredictor, sentence, grammaInSentenceIndex, [None, '*'])

        if ud_gramma.mood == 'Mood=Ind': mood = 'i'
        if ud_gramma.mood == 'Mood=Cnd': mood = 'i'
        if ud_gramma.mood == 'Mood=Imp': mood = 'm'

        if pos == 'V':
            aspectual = self.predict(self.aspectualPredictor, sentence, grammaInSentenceIndex, [None, 'm', 'b'])

        if ud_gramma.person == 'Person=1': person = '1'
        if ud_gramma.person == 'Person=2': person = '2'
        if ud_gramma.person == 'Person=3': person = '3'

        if ud_gramma.tense == 'Tense=Past': tense = 's'
        elif ud_gramma.tense == 'Tense=Pres': tense = 'p'
        elif ud_gramma.tense == 'Tense=Fut': tense = 'f'
        else:
            tense = self.predict(self.tensePredictor, sentence, grammaInSentenceIndex, [None, '*'])

        if pos == 'V':
            if ud_gramma.verbForm == 'VerbForm=Fin': verbForm = None
            elif ud_gramma.verbForm == 'VerbForm=Inf': verbForm = 'n'
            elif ud_gramma.verbForm == 'VerbForm=Part': verbForm = 'p'
            elif ud_gramma.verbForm == 'VerbForm=Trans': verbForm = 'g'
            else:
                verbForm = self.predict(self.verbFormPredictor, sentence, grammaInSentenceIndex, [None, 'x'])

        if pos == 'V' and (verbForm == 'p' or verbForm == 'g'):
            fullForm = self.predict(self.fullFormPredictor, sentence, grammaInSentenceIndex, ['s', 'f'])

        if ud_gramma.voice == 'Voice=Act': voice = 'a'
        if ud_gramma.voice == 'Voice=Mid': voice = 'p'
        if ud_gramma.voice == 'Voice=Pass': voice = 's'

        if ud_gramma.degree == 'Degree=Pos': degree = 'p'
        if ud_gramma.degree == 'Degree=Cmp': degree = 'c'
        if ud_gramma.degree == 'Degree=Sup': degree = 's'

        # модель для переходности
        if pos == 'V':
            trans = self.predict(self.transPredictor, sentence, grammaInSentenceIndex, [None, 'y', 'n'])
        
        if pos == 'P':
            # модель для систаксического типа прилагательного
            syntaxType = self.predict(self.syntaxTypePredictor, sentence, grammaInSentenceIndex, [None, 'n', 'a', 'p', 'r'])
            # модель для разряда местоимения
            categoryOfAdjective = self.predict(self.categoryOfAdjectivePredictor, sentence, grammaInSentenceIndex, [None, 'p', 'd', 'i', 's', 'q', 'x', 'z', 'n'])

        # модель для признака у части речи X
        if pos == 'X':
            typeOfAnother = self.predict(self.typeOfAnotherPredictor, sentence, grammaInSentenceIndex, [
                None,
                'u',
                'd',
                'c',
                'p',
                'f',
                'z',
                'r',
                's',
                'g',
                't',
                '-',
            ])
        
        if pos == 'S':
            # модель для типа предлога
            typeOfAdposition = self.predict(self.typeOfAdpositionPredictor, sentence, grammaInSentenceIndex, ['p', 't'])
            # модель для структуры предлога
            structureOfAdposition = self.predict(self.structureOfAdpositionPredictor, sentence, grammaInSentenceIndex, ['s', 'c'])
        if pos == 'M':
            # модель для разряда числительного
            categoryOfNumeral = self.predict(self.categoryOfNumeralPredictor, sentence, grammaInSentenceIndex, ['c', 'l', 'o', '*'])
            # модель для формы записи числительного
            formOfNumeral = self.predict(self.formOfNumeralPredictor, sentence, grammaInSentenceIndex, ['l', 'd', 'r'])

        gramma = Gramma(
            ud_gramma.word,
            ud_gramma.lemma if ud_gramma.lemma else "",
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