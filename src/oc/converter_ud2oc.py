from src.common.gramma import Gramma
from src.oc.predictor import OCPrecitor
from src.common.nnPredictor import NnPredictor
import sys
import re

class UD2OCConverter():
    def __init__(self, use_prediction, use_nn):
        self.use_nn = use_nn
        if (use_nn):
            self.posPredictor = NnPredictor('oc', 'pos')
            self.casePredictor = NnPredictor('oc', 'case')
            self.transPredictor = NnPredictor('oc', 'trans')
            self.invlPredictor = NnPredictor('oc', 'invl')
            self.verbFormPredictor = NnPredictor('oc', 'verbForm')
            self.degreePredictor = NnPredictor('oc', 'degree')
            # self.additionalPredictor = NnPredictor('oc', 'additional')
            self.additionalPredictor = OCPrecitor('additional')
            self.nameTypePredictor = OCPrecitor('nameType')
        else:
            self.posPredictor = OCPrecitor('pos')
            self.casePredictor = OCPrecitor('case')
            self.transPredictor = OCPrecitor('trans')
            self.invlPredictor = OCPrecitor('invl')
            self.verbFormPredictor = OCPrecitor('verbForm')
            self.degreePredictor = OCPrecitor('degree')
            self.additionalPredictor = OCPrecitor('additional')
            self.nameTypePredictor = OCPrecitor('nameType')

        self.use_prediction = use_prediction

    def convertGramma(
        self, 
        ud_gramma, 
        sentence, 
        grammaInSentenceIndex, 
        predictedPosTags = None,
        predictedCaseTags = None,
        predictedTransTags = None,
        predictedInvlTags = None,
        predictedVerbFormTags = None,
        predictedDegreeTags = None,
        predictedAdditionalTags = None
    ):
        pos = 'UNKN'
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

        if ud_gramma.gender == 'Gender=Masc': gender = 'masc'
        if ud_gramma.gender == 'Gender=Fem': gender = 'femn'
        if ud_gramma.gender == 'Gender=Neut': gender = 'neut'
        if ud_gramma.animacy == 'Animacy=Anim': animacy = 'anim'
        if ud_gramma.animacy == 'Animacy=Inan': animacy = 'inan'
        if ud_gramma.number == 'Number=Sing': number = 'sing'
        if ud_gramma.number == 'Number=Plur': number = 'plur'
        if ud_gramma.number == 'Number=Ptan': number = 'Pltm'
        if ud_gramma.number == 'Number=Coll': number = 'Sgtm'
        if ud_gramma.case == 'Case=Nom': case = 'nomn' # self.casePredictor.predict(sentence, grammaInSentenceIndex) if self.use_prediction else 'nomn'
        if ud_gramma.case == 'Case=Gen': case = 'gent' # self.casePredictor.predict(sentence, grammaInSentenceIndex) if self.use_prediction else 'gent'
        if ud_gramma.case == 'Case=Dat': case = 'datv'
        if ud_gramma.case == 'Case=Acc': case = 'accs' # self.casePredictor.predict(sentence, grammaInSentenceIndex) if self.use_prediction else 'accs'
        if ud_gramma.case == 'Case=Loc': case = 'loct' # self.casePredictor.predict(sentence, grammaInSentenceIndex) if self.use_prediction else 'loct'
        if ud_gramma.case == 'Case=Ins': case = 'ablt'
        if ud_gramma.aspect == 'Aspect=Imp': aspect = 'impf'
        if ud_gramma.aspect == 'Aspect=Perf': aspect = 'perf'
        if ud_gramma.mood == 'Mood=Ind': mood = 'indc'
        if ud_gramma.mood == 'Mood=Cnd': mood = 'indc'
        if ud_gramma.mood == 'Mood=Imp': mood = 'impr'
        if ud_gramma.person == 'Person=1': person = '1per'
        if ud_gramma.person == 'Person=2': person = '2per'
        if ud_gramma.person == 'Person=3': person = '3per'
        if ud_gramma.tense == 'Tense=Past': tense = 'past'
        if ud_gramma.tense == 'Tense=Pres': tense = 'pres'
        if ud_gramma.tense == 'Tense=Fut': tense = 'futr'
        if ud_gramma.voice == 'Voice=Act': voice = 'actv'
        if ud_gramma.voice == 'Voice=Mid': voice = 'actv'
        if ud_gramma.voice == 'Voice=Pass': voice = 'pssv'
        if ud_gramma.nameType == 'NameType=Geo': nameType = 'Geox'
        if ud_gramma.nameType == 'NameType=Prs': nameType = self.predict(self.nameTypePredictor, sentence, grammaInSentenceIndex, ['Patr', 'Name'])
        if ud_gramma.nameType == 'NameType=Giv': nameType = self.predict(self.nameTypePredictor, sentence, grammaInSentenceIndex, ['Patr', 'Name'])
        if ud_gramma.nameType == 'NameType=Sur': nameType = 'Surn'
        if ud_gramma.nameType == 'NameType=Com': nameType = 'Orgn'
        if ud_gramma.nameType == 'NameType=Pro': nameType = 'Trad'
        if ud_gramma.nameType == 'NameType=Oth': nameType = 'Init'
        if ud_gramma.verbForm == 'VerbForm=Inf': verbForm = 'INFN'
        elif ud_gramma.verbForm == 'VerbForm=Part': 
            if self.use_nn:
                verbForm = self.extractTagFromNNPrediction(
                    predictedVerbFormTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedVerbFormTags) else None, 
                    ['PRTF', 'PRTS']
                )
            else: 
                verbForm = self.predict(self.verbFormPredictor, sentence, grammaInSentenceIndex, ['PRTF', 'PRTS'])
        elif ud_gramma.verbForm == 'VerbForm=Trans': verbForm = 'GRND'
        else: 
            if self.use_nn:
                verbForm = self.extractTagFromNNPrediction(
                    predictedVerbFormTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedVerbFormTags) else None,
                    [None, 'Fimp', 'V-sh']
                )
            else:
                verbForm = self.predict(self.verbFormPredictor, sentence, grammaInSentenceIndex, [None, 'Fimp', 'V-sh'])
        if self.use_nn:
            degree = self.extractTagFromNNPrediction(
                predictedDegreeTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedDegreeTags) else None, 
                [None, 'ADVB', 'Cmp2', 'V-ej', 'Supr']
                )
        else:
            degree = self.predict(self.degreePredictor, sentence, grammaInSentenceIndex, [None, 'ADVB', 'Cmp2', 'V-ej', 'Supr'])

        if ud_gramma.pos == 'NOUN':  pos = 'NOUN'
        if ud_gramma.pos == 'PROPN': pos = 'NOUN' 
        if ud_gramma.pos == 'PRON':  pos = 'NPRO'
        if ud_gramma.pos == 'DET':   pos = 'NPRO'
        if ud_gramma.pos == 'ADJ':   
            if self.use_nn:
                pos = self.extractTagFromNNPrediction(
                    predictedPosTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedPosTags) else None, 
                    ['ADJF', 'ADJS', 'COMP']
                )
            else:
                pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['ADJF', 'ADJS', 'COMP'])
        
        if ud_gramma.pos == 'NUM':   pos = 'NUMR'
        if ud_gramma.pos == 'ADV':   pos = 'ADVB'
        if ud_gramma.pos == 'AUX':   pos = 'VERB'
        # if ud_gramma.pos == 'VERB' and ud_gramma.verbForm == 'VerbForm=Inf': pos = 'INFN' 
        # if ud_gramma.pos == 'VERB' and ud_gramma.verbForm == 'VerbForm=Part': 
        #     if self.use_nn:
        #         pos = self.extractTagFromNNPrediction(
        #             predictedPosTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedPosTags) else None, 
        #             ['VERB', 'INFN', 'PRTF', 'PRTS', 'GRND']
        #             )
        #     else:
        #         pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['VERB', 'INFN', 'PRTF', 'PRTS', 'GRND'])
        
        # if ud_gramma.pos == 'VERB' and ud_gramma.verbForm == 'VerbForm=Trans': pos = 'GRND' 
        if ud_gramma.pos == 'VERB':  
            if self.use_nn:
                pos = self.extractTagFromNNPrediction(
                    predictedPosTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedPosTags) else None, 
                    ['VERB', 'INFN', 'PRTF', 'PRTS', 'GRND']
                )
            else:
                pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['VERB', 'INFN', 'PRTF', 'PRTS', 'GRND'])
        
        if ud_gramma.pos == 'CONJ':  pos = 'CONJ'
        if ud_gramma.pos == 'ADP':   pos = 'PREP'
        if ud_gramma.pos == 'INTJ':  pos = 'INTJ'
        if ud_gramma.pos == 'PART':  pos = 'PRCL'
        if ud_gramma.pos == 'SYM':   pos = 'PNCT'
        if ud_gramma.pos == 'PUNCT': pos = 'PNCT'
        if ud_gramma.pos == 'X':
            pattern = re.compile("^[0-9.,\-\+]+$")
            if False and pattern.match(ud_gramma.word):
                pos = 'NUMB'
            elif self.use_nn: 
                pos = self.extractTagFromNNPrediction(
                    predictedPosTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedPosTags) else None, 
                    ['UNKN', 'NUMB', 'LATN', 'ROMN']
                )
            else:
                pos = self.predict(self.posPredictor, sentence, grammaInSentenceIndex, ['UNKN', 'NUMB', 'LATN', 'ROMN'])
        
        if self.use_nn:
            trans = self.extractTagFromNNPrediction(
                predictedTransTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedTransTags) else None, 
                [None, 'tran', 'intr']
            )
            invl = self.extractTagFromNNPrediction(
                predictedInvlTags[grammaInSentenceIndex] if grammaInSentenceIndex < len(predictedInvlTags) else None, 
                [None, 'incl', 'excl']
            )
        else:
            trans = self.predict(self.transPredictor, sentence, grammaInSentenceIndex, [None, 'tran', 'intr'])
            invl = self.predict(self.invlPredictor, sentence, grammaInSentenceIndex, [None, 'incl', 'excl'])
        additinalTags = self.additionalPredictor.predict(sentence, grammaInSentenceIndex) if self.use_prediction else ""
        additional = additinalTags.split(",") if additinalTags != "" else []               

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
            additional
        )
        
        return gramma


    def convert(self, ud_sentences):
        oc_sentences = []
        posTags = None if not self.use_nn else self.posPredictor.predict(ud_sentences)
        caseTags = None if not self.use_nn else self.casePredictor.predict(ud_sentences)
        transTags = None if not self.use_nn else self.transPredictor.predict(ud_sentences)
        invlTags = None if not self.use_nn else self.invlPredictor.predict(ud_sentences)
        verbFormTags = None if not self.use_nn else self.verbFormPredictor.predict(ud_sentences)
        degreeTags = None if not self.use_nn else self.degreePredictor.predict(ud_sentences)
        additionalTags = None # if not self.use_nn else self.additionalPredictor.predict(ud_sentences)

        for sentenceIndex in range(len(ud_sentences)):
            sys.stdout.write("convert %s/%s\r" % (sentenceIndex, len(ud_sentences)))
            sys.stdout.flush()
            ud_sentence = ud_sentences[sentenceIndex]
            oc_sentence = []
            for index in range(len(ud_sentence)):
                ud_gramma = ud_sentence[index]
                posTagsForSentence = (posTags[sentenceIndex] if posTags else [])
                caseForSentence = (caseTags[sentenceIndex] if caseTags else [])
                transForSentence = (transTags[sentenceIndex] if transTags else [])
                invlForSentence = (invlTags[sentenceIndex] if invlTags else [])
                verbFormForSentence = (verbFormTags[sentenceIndex] if verbFormTags else [])
                degreeForSentence = (degreeTags[sentenceIndex] if degreeTags else [])
                additionalForSentence = (additionalTags[sentenceIndex] if additionalTags else [])
                oc_gramma = self.convertGramma(
                    ud_gramma, 
                    ud_sentence, 
                    index, 
                    posTagsForSentence,
                    caseForSentence,
                    transForSentence,
                    invlForSentence,
                    verbFormForSentence,
                    degreeForSentence,
                    additionalForSentence
                )
                oc_sentence.append(oc_gramma)
            oc_sentences.append(oc_sentence)

        
        
        return oc_sentences

    def predict(self, predictor, sentence, grammaInSentenceIndex, variants):
        if not self.use_prediction:
            return variants[0]
        prediction = predictor.predict(sentence, grammaInSentenceIndex)
        if not prediction or prediction not in variants:
            return variants[0]
        else:
            return prediction

    def predictTagsWithNN(self, predictor, sentences):
        print("Predict tags")
        predictedTags = predictor.predict(sentences)
        return predictedTags

    def extractTagFromNNPrediction(self, predictedTag, possibleTags):
        if not self.use_prediction:
            return possibleTags[0]
        if not predictedTag or predictedTag not in possibleTags:
            return possibleTags[0]
        else:
            return predictedTag
