# -*- coding: utf-8 -*-
# Author Samhaa R. El-Beltagy
# Version 1.0

import re
import codecs

def normalizeText(text):
    """
        normalizes all forms to alf to ا, converts ة to ه, and ى to ي.  It also converts new lines and tabs to a single space  
        and seperates common punctuation marks from text 
    """	


    search = ["أ", "إ", "آ", "ة", "_", "-", "/", ".", "،", " و ", " يا ", '"', "ـ", "'", "ى", "\\", '\n', '\t','&quot;', '?', '؟', '!']
    replace = ["ا", "ا", "ا", "ه", " ", " ", "", "", "", " و", " يا", "", "", "", "ي", "", ' ', ' ', ' ', ' ? ', ' ؟ ',  ' ! ']

    #search = ["آ", "إ", "أ", "ة"]
    #replace = ["ا", "ا", "ا", "ه"]

    for i in range(0, len(search)):
        text = text.replace(search[i], replace[i])
    return text

def removeTashkeel(text): 
    # Removes Tashkeel from input text

    
    p_tashkeel = re.compile(r'[\u0616-\u061A\u064B-\u0652\u06D6-\u06ED\u08F0-\u08F3\uFC5E-\uFC63\u0670]')
    text = re.sub(p_tashkeel,"", text)
    return text


def getCount(d, key):
    c = d.get(key)
    if c == None:
        return 0
    return c


def genNgramsInBuckets(txt, grams):
    #Takes as input some text represented as a list, and generates all possible (uni-grams to n-grams) ngrams based on the grams parameter. 
    #The function returns a list of dictionaries of size 'grams'. The first entry represents the dict of all uni-grams and their counts, 
    #The second, all bi-grams and their counts, and so on. 
    #This works on any text, not just Arabic.  For example given the following code:
    #     x ="test to test the function".split()
    #     v =ArUtils.genNgramsInBuckets(x,3)
    #     print(v)
    #The output will be:
    #     [{'test': 2, 'to': 1, 'the': 1, 'function': 1}, {'test to': 1, 'to test': 1, 'test the': 1, 'the function': 1},
    #      {'test to test': 1, 'to test the': 1, 'test the function': 1}]


    result = []
    for x in range(grams):
        result.append({})
    if grams < 1:
        return

    cnt = 0
    j = 0
    for i in txt:
        result[0][i] = getCount(result[0], i) + 1
        y = 1
        # print(y,cnt,grams)
        while y <= cnt and y < grams:
            np = []
            for u in range(y):
                np.append(txt[j - y + u])
            np.append(i)
            # np = tuple(np)
            np = " ".join(np)
            # print( np)
            result[y][np] = getCount(result[y], np) + 1
            y = y + 1
        j = j + 1
        cnt = cnt + 1
    return result 

def genNgrams(txt, grams):
    #Takes as input some text represented as a list, and generates all possible (uni-grams to n-grams) ngrams based on the grams parameter.
    #The function returns a dictionary of the generated n-grams and their counts.
    #The secong, all uni-grams and their counts, and so on. 
    #     x ="test to test the function".split()
    #     v =ArUtils.genNgrams(x,3)
    #     print(v)
    #The output will be:
    #     {'test': 2, 'to': 1, 'test to': 1, 'to test': 1, 'test to test': 1, 'the': 1, 'test the': 1, 'to test the': 1, 
    #      'function': 1, 'the function': 1, 'test the function': 1}

    
    result = {}

    cnt = 0
    j = 0
    for i in txt:
        result[i] = getCount(result, i) + 1
        y = 1
        # print(y,cnt,grams)
        while y <= cnt and y < grams:
            np = []
            for u in range(y):
                np.append(txt[j - y + u])
            np.append(i)
            # np = tuple(np)
            np = " ".join(np)
            # print( np)
            result[np] = getCount(result, np) + 1
            y = y + 1
        j = j + 1
        cnt = cnt + 1
    return result 

def getContents(fname, normalize=True, removeTashkeel=True):
    #Simply reads the contents of a utf-encocded Arabic file and returns them as a string
    #There two optional parameters allow the user to configure whether s/he wants the contents
    #normalized and diacritics (Tashkeel) removed or not.
    
    f = codecs.open(fname, "r", "utf-8")
    #f = open(fname, "r")
    contents  = f.read()
    if normalize:
        contents = normalizeText(contents)
    if removeTashkeel:
        contents = removeTashkeel(contents)
    return contents
