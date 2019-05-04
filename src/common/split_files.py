def split_files(source, targetTrain, targetTest, ratio = 0.8):
    sentences = []
    with open(source, 'r') as sourceFile:
        sentence = []
        for line in sourceFile:
            if line == "BEGIN\n":
                continue
            elif line == "END\n":
                sentences.append(sentence)
                sentence = []
                continue
            sentence.append(line)

    trainSentences = sentences[:int(len(sentences) * ratio)]
    testSentences = sentences[int(len(sentences) * ratio):]
    with open(targetTrain, 'w') as file:
        for sentence in trainSentences:
            file.write("BEGIN\n")
            for line in sentence:
                file.write(line)
            file.write("END\n")

    with open(targetTest, 'w') as file:
        for sentence in testSentences:
            file.write("BEGIN\n")
            for line in sentence:
                file.write(line)
            file.write("END\n")
            