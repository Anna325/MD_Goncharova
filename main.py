import sys
"""
    1) Парсим файл в UD
    2) Переводим файл в OpenCorpora
    3) Переводим файл обратно в UD
    4) Сравниваем UD1 и UD2
"""

from src.oc.train import train_all_models as train_all_models_oc
from src.nkry.train import train_all_models as train_all_models_nkry
from src.gikry.train import train_all_models as train_all_models_gikry
from src.ud.train import train_all_models as train_all_models_ud
from src.oc.parser import parse_opencorpora
from src.oc.converter_oc2ud import OC2UDConverter
from src.oc.converter_ud2oc import UD2OCConverter
from src.nkry.converter_nkry2ud import NKRY2UDConverter
from src.nkry.converter_ud2nkry import UD2NKRYConverter
from src.gikry.converter_gikry2ud import GIKRY2UDConverter
from src.gikry.converter_ud2gikry import UD2GIKRYConverter
from src.common.loader import loadOCGrammasFromFile, loadNKRYGrammasFromFile, loadUDGrammasFromFile, loadGIKRYGrammasFromFile
from src.oc.saver import OCSaver
from src.nkry.saver import NKRYSaver
from src.gikry.saver import GIKRYSaver
from src.common.differ import diff_files
from src.common.merge import merge_files
from src.ud.parser import parse_ud
from src.ud.saver import UDSaver
from src.gikry.parser import parse_gikry
from src.common.gramma_differ import diff_sentences
from src.training.classifier.trainer import ClassifierTrainer
from src.common.split_files import split_files

from os import listdir
from os.path import isfile, join

from src.nkry.parser import parse_nkry

command = sys.argv[1] if len(sys.argv) > 1 else 'reconvert_oc'
secondArg = sys.argv[2] if len(sys.argv) > 2 else None
thirdArg = sys.argv[3] if len(sys.argv) > 3 else None

if (command == 'reconvert'):
    if secondArg == 'oc':
        print("Step 1. Save original file with saver")
        saver = OCSaver()
        # Конвертирование OC-грамем в UD-грамемы
        original_oc_sentences = loadOCGrammasFromFile('tmp/oc/test.txt')
        saver.save('tmp/oc/test_non_converted.txt', original_oc_sentences)
        print("Step 2. Convert OC to UD")
        oc2ud_converter = OC2UDConverter(True)
        ud_sentences = oc2ud_converter.convert(original_oc_sentences)

        # Конвертация обратно из UD-грамем в OC-грамемы
        print("Step 3. Create UD2OC Converter")
        ud2oc_converter = UD2OCConverter(True, False)
        print("Step 4. Convert UD to OC")
        oc_sentences = ud2oc_converter.convert(ud_sentences)

        # Сохранение грамем в OC-файл
        print("Step 5. Save converted OC file")
        saver.save('tmp/oc/test_converted.txt', oc_sentences)

        print("Step 6. Diff original and converted file")
        # Сравнивание исходного OC-файла и получившегося OC-файла
        diff_sentences(original_oc_sentences, oc_sentences)
        diff_files('tmp/oc/test_non_converted.txt', 'tmp/oc/test_converted.txt')
    elif secondArg == 'nkry':
        print("Step 1. Save original file with saver")
        saver = NKRYSaver()
        # Конвертирование NKRY-грамем в UD-грамемы
        original_nkry_sencentes = loadNKRYGrammasFromFile('tmp/nkry/test.txt')
        saver.save('tmp/nkry/test_not_converted.txt', original_nkry_sencentes)
        print("Step 2. Convert NKRY to UD")
        nkry2ud_converter = NKRY2UDConverter(True)
        ud_sentences = nkry2ud_converter.convert(original_nkry_sencentes)

        # Конвертация обратно из UD-грамем в NKRY-грамемы
        print("Step 3. Create UD2NKRY Converter")
        ud2nkry_converter = UD2NKRYConverter(True)
        print("Step 4. Convert UD to NKRY")
        nkry_sentences = ud2nkry_converter.convert(ud_sentences)

        # Сохранение грамем в OC-файл
        print("Step 5. Save converted NKRY file")
        saver.save('tmp/nkry/test_converted.txt', nkry_sentences)

        print("Step 6. Diff original and converted file")
        # Сравнивание исходного OC-файла и получившегося OC-файла
        diff_sentences(original_nkry_sencentes, nkry_sentences)
        diff_files('tmp/nkry/test_not_converted.txt', 'tmp/nkry/test_converted.txt')
    elif secondArg == 'gikry':
        print("Step 1. Load original file")
        saver = GIKRYSaver()
        original_gikry_sentences = loadGIKRYGrammasFromFile('tmp/gikry/test.txt')
        print("Step 2. Save original grammas with saver")
        saver.save('tmp/gikry/test_not_converted.txt', original_gikry_sentences)
        print("Step 3. Convert GIKRY to UD")
        gikry2ud_converter = GIKRY2UDConverter(True)
        ud_sentences = gikry2ud_converter.convert(original_gikry_sentences)
        print("Step 4. Convert UD to GIKRY")
        ud2gikry_converter = UD2GIKRYConverter(True)
        gikry_sentences = ud2gikry_converter.convert(ud_sentences)
        print("Step 5. Save GIKRY sentences")
        saver.save('tmp/gikry/test_converted.txt', gikry_sentences)

        print("Step 6. Diff original and converted file")
        diff_sentences(original_gikry_sentences, gikry_sentences)
        diff_files('tmp/gikry/test_not_converted.txt', 'tmp/gikry/test_converted.txt')
        
    elif secondArg == 'ud':
        print("Step 1. Save original file with saver")
        saver = UDSaver()
        original_ud_sencentes = loadUDGrammasFromFile('tmp/ud/test.txt')
        saver.save('tmp/ud/test_not_converted.txt', original_ud_sencentes)
        # # Конвертирование UD-грамем в OC-грамемы
        print("Step 2. Convert UD to OC")
        ud2oc_converter = UD2OCConverter(True, False)
        oc_sentences = ud2oc_converter.convert(original_ud_sencentes)

        # # Конвертация обратно из UD-грамем в NKRY-грамемы
        print("Step 3. Create OC2UD Converter")
        od2ud_converter = OC2UDConverter(True)
        print("Step 4. Convert OC to UD")
        ud_sentences = od2ud_converter.convert(oc_sentences)

        # # Сохранение грамем в UD-файл
        print("Step 5. Save converted UD file")
        saver.save('tmp/ud/test_converted.txt', ud_sentences)

        print("Step 6. Diff original and converted file")
        # Сравнивание исходного UD-файла и получившегося UD-файла
        diff_sentences(original_ud_sencentes, ud_sentences)
        diff_files('tmp/ud/test_not_converted.txt', 'tmp/ud/test_converted.txt')

elif command == 'prepare':
    if secondArg == 'nkry':
    # Конвертация оригинальных NKRY-файлов в внутренний формат
        path = 'data/NKRY'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            print("Parse NKRY file %s" % file)
            filename = join(path, file)
            text = parse_nkry(filename)
            print("Write parsed data for %s" % file)
            with open('tmp/nkry/texts/%s.txt' % file.replace('.xhtml', '.txt'), 'w') as result:
                result.write(text)
                result.close()

        # Слияние всех полученных NKRY-файлов в один
        tmpPath = 'tmp/nkry/texts'
        files = [join(tmpPath, f) for f in listdir(tmpPath) if isfile(join(tmpPath, f))]
        print("Merge %s files" % len(files))
        merge_files(files, 'tmp/nkry/merged.txt')
        split_files('tmp/nkry/merged.txt', 'tmp/nkry/train.txt', 'tmp/nkry/test.txt')

    elif secondArg == 'gikry':
        # Конвертация оригинальных NKRY-файлов в внутренний формат
        path = 'data/GIKRY'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file in files:
            print("Parse GIKRY file %s" % file)
            filename = join(path, file)
            text = parse_gikry(filename)
            print("Write parsed data for %s" % file)
            with open("tmp/gikry/texts/%s.txt" % file, 'w') as result:
                result.write(text)
                result.close()
        
        tmpPath = 'tmp/gikry/texts'
        files = [join(tmpPath, f) for f in listdir(tmpPath) if isfile(join(tmpPath, f))]
        print("Merge %s files" % len(files))
        merge_files(files, 'tmp/gikry/merged.txt')
        split_files('tmp/gikry/merged.txt', 'tmp/gikry/train.txt', 'tmp/gikry/test.txt')

    elif secondArg == 'oc':
        # Парсинг исходного файла  opencorpora из XML в строчную структуру
        print("Parse opencorpora file")
        filename = "data/OpenCorpora/annot.opcorpora.xml"
        text = parse_opencorpora(filename)
        print("Write parsed data")
        with open('tmp/oc/opencorpora_parsed.txt', 'w') as result:
            result.write(text)
            result.close()
        split_files('tmp/oc/opencorpora_parsed.txt', 'tmp/oc/train.txt', 'tmp/oc/test.txt')

    elif secondArg == 'ud':
        print("Parse UD file")
        filename = 'data/UD/text.txt' if thirdArg != 'small' else 'data/UD/text.small.txt'
        print(filename)
        text = parse_ud(filename)
        print('Write parsed data')
        with open('tmp/ud/parsed.txt', 'w') as result:
            result.write(text)
            result.close()
        split_files('tmp/ud/parsed.txt', 'tmp/ud/train.txt', 'tmp/ud/test.txt')
        
    else:
        print("Неизвестная разметка %s, используйте nkry, oc" % secondArg)

elif command == 'train':
    if secondArg == 'oc':
        # Тренировка всех OC-моделей на подготовленном тексте, который парсился выше
        train_all_models_oc('tmp/oc/train.txt')
    elif secondArg == 'nkry':
        train_all_models_nkry('tmp/nkry/train.txt')
    elif secondArg == 'gikry':
        train_all_models_gikry('tmp/gikry/train.txt')
    elif secondArg == 'ud':
        train_all_models_ud('tmp/ud/train.txt')
    else:
        print("Неизвестная разметка %s, используйте nkry, oc" % secondArg)

elif command == 'train_classifier':
    tagToTrain = thirdArg
    if not tagToTrain:
        print("Specify tag for training")
        quit()

    if secondArg == 'oc':
        # Тренировка нейронной сети на подготовленном тексте
        textFilename = 'tmp/oc/train.txt'
        sentences = loadOCGrammasFromFile(textFilename)
        trainer = ClassifierTrainer(sentences, tagToTrain)
        trainer.train('model/oc/classifier/%s/' % tagToTrain)

elif command == 'count':
    markup = secondArg
    testFile = 'tmp/%s/test.txt' % markup
    trainFile = 'tmp/%s/train.txt' % markup
    testSentences = []
    trainSentences = []
    if markup == 'oc':
        testSentences = loadOCGrammasFromFile(testFile)
        trainSentences = loadOCGrammasFromFile(trainFile)
    elif markup == 'ud':
        testSentences = loadUDGrammasFromFile(testFile)
        trainSentences = loadUDGrammasFromFile(trainFile)
    elif markup == 'nkry':
        testSentences = loadNKRYGrammasFromFile(testFile)
        trainSentences = loadNKRYGrammasFromFile(trainFile)
    elif markup == 'gikry':
        testSentences = loadGIKRYGrammasFromFile(testFile)
        trainSentences = loadGIKRYGrammasFromFile(trainFile)
    
    testWords = 0
    trainWords = 0
    for sentence in testSentences:
        for word in sentence:
            testWords += 1
    for sentence in trainSentences:
        for word in sentence:
            trainWords += 1
    print("Train words: %s. Test words: %s" % (trainWords, testWords))

else:
    print("Unknown command %s" % command)


