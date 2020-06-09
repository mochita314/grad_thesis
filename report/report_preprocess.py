# the code for proceccing reports

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
        finding = sheet.cell(i,6).value.split()
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

def adjust_word(word):
    '''
    remove unnecessary symbols from word
    '''
    word_lst = []
    if word[-1] == '.' or word[-1] == ',':
        '''
        when symbols are at the end of the word
        '''
        if len(word) >= 2:
            if word[-2] == '.' or word[-2] == ',':
                word = word[:-2]
            else:
                word = word[:-1]
        else:
            return word_lst
    elif '.' in word:
        '''
        when period is in the middle of the word
        '''
        index = word.index('.')
        word1 = word[:index]
        word2 = word[index+1:]
        word_lst.append(word1)
        word_lst.append(word2)
    else:
        word_lst.append(word)
    return word_lst

def make_dct(lst):
    '''
    the function to make word dictionary from the list
    '''
    dct = {}
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            word = lst[i][j].lower()
            word_lst = adjust_word(word)  
            for w in word_lst:
                num = word_to_number(w)
                key,is_found = found_word(dct,num,w)
                if not is_found:
                    dct[key] = w
    return dct

def save_obj(obj,path):
    with open(path,mode='wb') as f:
        pickle.dump(obj,f)

def load_obj(path):
    with open(path,mode='rb') as f:
        data = pickle.load(f)
        return data

if __name__ == '__main__':
    lst = load_report('/data/unagi0/kizawa/IU_X_ray/indiana_reports.xls','indiana_reports')
    dct = make_dct(lst)
    '''
    cnt = 0
    for key in dct:
        if cnt < 200:
            print(dct[key])
        else:
            break
        cnt += 1
    '''
    save_obj(lst,'./data/lst.pickle')
    save_obj(lst,'./data/dct.pickle')