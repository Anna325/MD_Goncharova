def merge_files(files, resultFile):
    with open(resultFile, 'w') as result:
        for file in files:
            with open(file, 'r') as f:
                for line in f:
                    result.write(line)
                result.write("\n")
        result.close()
