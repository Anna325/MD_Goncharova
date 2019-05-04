class Gramma():
    def __init__(
        self,
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
        fullForm = None,
        nounType = None,
        additionalCase = None,
        aspectual = None,
        categoryOfAdjective = None,
        syntaxType = None,
        categoryOfNumeral = None,
        formOfNumeral = None,
        typeOfAdposition = None,
        structureOfAdposition = None,
        typeOfAnother = None
    ):
        self.word = word
        self.lemma = lemma
        self.pos = pos
        self.gender = gender
        self.animacy = animacy
        self.number = number
        self.case = case
        self.aspect = aspect
        self.mood = mood
        self.person = person
        self.poss = poss
        self.reflex = reflex
        self.tense = tense
        self.verbForm = verbForm
        self.voice = voice
        self.degree = degree
        self.nameType = nameType
        self.trans = trans
        self.invl = invl
        self.additional = additional
        self.fullForm = fullForm
        self.nounType = nounType
        self.additionalCase = additionalCase
        self.aspectual = aspectual
        self.categoryOfAdjective = categoryOfAdjective
        self.syntaxType = syntaxType
        self.categoryOfNumeral = categoryOfNumeral
        self.formOfNumeral = formOfNumeral
        self.typeOfAdposition = typeOfAdposition
        self.structureOfAdposition = structureOfAdposition
        self.typeOfAnother = typeOfAnother