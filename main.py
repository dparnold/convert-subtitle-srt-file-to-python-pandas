import pandas as pd
import time
import os

import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)


def is_integer(i):
    try:
        int(i)
        return True
    except ValueError:
        return False


def wordcount_from_srt(filename):
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
        # it is way faster if you first create a dictionary
        wordcount = {}
        text = ""
        content = f.readlines()
        for line in content:
            split = line.split("-->")
            if (not is_integer(line)) and (len(line.split("-->")) == 1) and (line != "\n"):
                text = text + " " + line
            elif line == "\n":
                text = text.replace('<i>', '').replace("</i>", '').replace('"', '').replace(',', '').replace('.',
                                                                                                             '').replace(
                    '!', '').replace('?', '').replace('-', '').replace("\n", '')
                for word in text.split(' '):
                    word = word.lower()
                    if word == '':
                        pass
                    elif word in wordcount:
                        wordcount[word] += 1
                    else:
                        wordcount[word] = 1
                text = ""
    return wordcount


def dict_to_pandas(dict):
    words = []
    count = []
    for key in dict:
        words.append(key)
        count.append(dict[key])
    df = pd.DataFrame(count, index=words, columns=['count'])
    df.sort_values(by='count', inplace=True)
    print(df)
    return df


def wordcount_from_folder(folder_name):
    outputdict = {}
    for filename in os.listdir(folder_name):
        if filename.endswith(".srt"):
            print(filename)
            newdict = wordcount_from_srt(folder + '/' + filename)
            if outputdict != {}:
                outputdict = merge_dicts(outputdict, newdict)
            else:
                outputdict = newdict
        print(outputdict)
    return outputdict


def merge_dicts(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1

if __name__ == "__main__":
    start_time = time.time()

    folder = 'srt_files'

    dict_to_pandas(wordcount_from_folder(folder))

    print("--- %s seconds ---" % (time.time() - start_time))


def wordcount_from_srt(filename):
    with open('srt_files/Importance Of Being Earnest The.srt', 'r', encoding='utf-8', errors='ignore') as f:
        # it is way faster if you first create a dictionary
        dict = {'id': [], 'time1': [], 'time2': [], 'text': []}
        wordcount = {}
        subtitle_number = 0
        time1 = 0
        time2 = 0
        text = ""
        counter = 1
        content = f.readlines()

        for line in content:
            split = line.split("-->")
            if is_integer(line):
                subtitle_number = int(line)
            elif len(split) > 1:
                time1 = split[0]
                time2 = split[1].strip("\n")
            elif line == "\n":
                dict['id'].append(subtitle_number)
                dict['time1'].append(time1)
                dict['time2'].append(time2)
                text = text.replace("\n", '')
                dict['text'].append(text)
                text = text.replace('<i>', '').replace("</i>", '').replace('"', '').replace(',', '').replace('.',
                                                                                                             '').replace(
                    '!', '').replace('?', '').replace('-', '')
                for word in text.split(' '):
                    word = word.lower()
                    if word == '':
                        pass
                    elif word in wordcount:
                        wordcount[word] += 1
                    else:
                        wordcount[word] = 1
                words = []
                count = []
                for key in wordcount:
                    words.append(key)
                    count.append(wordcount[key])
                text = ""
                counter = counter + 1
            else:
                text = text + " " + line
            return
