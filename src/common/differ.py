from src.common.errstats import ErrStats

def diff_files(filename1, filename2):
    errstat = ErrStats()
    with open(filename1, 'r') as file1:
        file1lines = file1.readlines()
    with open(filename2, 'r') as file2:
        file2lines = file2.readlines()
    
    total = 0
    errors = 0
    totalTags = 0 # подсчет ошибки по признакам, а не по словам
    tagsErrors = 0
    for index in range(len(file1lines)):
        total += 1
        str1 = file1lines[index].strip()
        str2 = file2lines[index].strip()
        if str1 == "" or str2 == "":
            continue
        if str1 != str2:
            # print("Error in diff: %s => %s" % (str1, str2))
            expectedTags = extract_tags(str1)
            actualTags = extract_tags(str2)
            if not expectedTags and not actualTags:
                raise Exception("No expectedTags and not actualTags\n%s\n%s" % (str1, str2))
            errstat.registerError(expectedTags, actualTags)
            errors += 1

            (extraTags, missingTags) = get_missing_and_extra_tags(expectedTags, actualTags)
            totalTags += len(expectedTags)
            tagsErrors += len(extraTags) + len(missingTags)
        else:
            expectedTags = extract_tags(str1)
            if expectedTags:
                totalTags += len(expectedTags)

    
    errstat.printErrors()
    print('Total lines: %s' % total)
    print("Errors: %s" % errors)
    print("Accuracy: %s" % round(100 - errors / total * 100, 2))
    tagsAccuracy = round(100 - tagsErrors / totalTags * 100, 2)
    # print("Total tags: %s. Tags errors: %s. Accuracy: %s" % (totalTags, tagsErrors, tagsAccuracy))

def extract_tags(string):
    # добьётесь	добиться VERB,Number=Plur,Aspect=Perf,Mood=Ind,Person=2,VerbForm=Fin,Voice=Act
    pieces = string.split("\t")
    if len(pieces) < 3:
        return None
    tags = pieces[2].strip().split(',')
    return tags

def get_missing_and_extra_tags(expectedTags, actualTags):
    if expectedTags and actualTags:
        missingTags = list(set(expectedTags) - set(actualTags))
        extraTags = list(set(actualTags) - set(expectedTags))    
    elif not expectedTags and actualTags and len(actualTags) > 0:
        extraTags = actualTags
        missingTags = []
    elif not actualTags and expectedTags and len(expectedTags) > 0:
        missingTags = expectedTags
        extraTags = []
    else:
        raise Exception("No normal tags and no predicted tags")

    return (extraTags, missingTags)