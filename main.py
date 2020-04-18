import pandas as pd
import time
import os

import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)



def wordcount_from_srt(filename):
    with open(filename, 'r', encoding='iso-8859-1', errors='replace') as f:
        # it is way faster if you first create a dictionary
        wordcount = {}
        text = ""
        content = f.readlines()
        replace_list = ['$', '*', '°', "'", '(', ')', '/']
        forbidden_substrings = ['©', 'ã', "color=", 'â']
        for line in content:
            split = line.split("-->")
            if (not is_integer(line)) and (len(line.split("-->")) == 1) and (line != "\n"):
                text = text + " " + line
            elif line == "\n":


                text = text.replace('<i>', '').replace("</i>", '').replace("</b>", '').replace("<b>", '').replace("</font>","").replace("#","").replace(">","").replace("<","").replace(":","").replace('"', '').replace(',', '').replace('.','').replace(
                    '!', '').replace('?', '').replace('-', '').replace("¿",'').replace("¡","").replace("[","").replace("]","").replace("{","").replace("}","").replace("\n", '')
                for token in replace_list:
                    text = text.replace(token,' ')
                for word in text.split(' '):
                    word = word.lower()

                    problem = False
                    for substring in forbidden_substrings:
                        problem = problem or (substring in word)
                    if (word == '') or (is_integer(word)) or problem:
                        pass
                    elif word in wordcount:
                        wordcount[word] += 1
                    else:
                        wordcount[word] = 1
                text = ""
    if 'the' in wordcount:
        if wordcount['the']>15:
            return wordcount
        else:
            return wordcount
    else:
        return wordcount


def dict_to_pandas(dict):
    words = []
    count = []
    for key in dict:
        words.append(key)
        count.append(dict[key])
    df = pd.DataFrame(list(zip(words, count)), columns=['word', 'count'])
    df.sort_values(by='count', ascending=True, inplace=True)
    df = df[df['count']>1]
    print(df.tail(10000))
    return df


def wordcount_from_folder(folder_name):
    outputdict = {}
    newdict= {}
    for filename in os.listdir(folder_name)[0:1000]:
        if filename.endswith(".srt"):
            print(filename)
            newdict = wordcount_from_srt(folder_name + '/' + filename)
            if outputdict != {}:
                outputdict = merge_dicts(outputdict, newdict)
            else:
                outputdict = newdict
        #print(outputdict)
    return outputdict


def merge_dicts(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1

def is_integer(i):
    try:
        int(i)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    start_time = time.time()

    folder = 'srt'

    df = dict_to_pandas(wordcount_from_folder(folder))
    df.to_csv("words.csv")

    print("--- %s seconds ---" % (time.time() - start_time))
