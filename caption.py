# the code for proceccing reports
# got inspiration from 'Deep Fragment Embeddings for Bidrectional Image Sentence Mapping [Karpathy+ NeurIPS2014]'

import xlrd
import pickle

def word_to_number(word):
    '''
    change word into number
    '''
    number = 0
    for w in word:
        number += ord(w)
    return number

def h1(key,mod):
    key = key % mod
    return key

def h2(key,mod):
    key = 1 + key % (mod - 1)
    return key

def h(key,i,mod):
    '''
    hash function
    i is the number of times of collision, initiallly set to be 0
    '''
    key = h1(key,mod) + i * h2(key,mod)
    return key

def load_report(data_path,sheet_name):
    '''
    load report file and make a list of findings
    '''
    report_data_file = xlrd.open_workbook(data_path)
    sheet = report_data_file.sheet_by_name(sheet_name)
    reports_list = []
    for i in range(1,3852):
        finding = sheet.cell(i,6).value
        #if i>=3845:
            #print(finding)
            #print('\n')
        reports_list.append(finding)
    return reports_list

def found_word(dct,num,word):
    '''
    check if the word is already in the dictionary or not
    '''
    for i in range(10**9):
        key = h(num,i,10**9+7)
        if dct.get(key) == word:
            return key,True
        elif dct.get(key) == None:
            return key,False
        else:
            pass

def make_dct(lst):
    '''
    the function to make word dictionary from the list
    '''
    dct = {}
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            word = lst[i][j]
            num = word_to_number(word)
            key,is_found = found_word(dct,num,word)
            if not is_found:
                dct[key] = word
    return dct

# lst = load_report('/data/unagi0/kizawa/IU_X_ray/indiana_reports.xls')