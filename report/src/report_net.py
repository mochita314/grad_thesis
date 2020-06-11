import torch
from torch.utils.data import DataLoader

from report_preprocess import *

class Report2vec:

    def __init__(self,name):

        self.name = name
        self.file_path = '../data/med_parsed.txt'
        self.type_path = '../data/dependency_type.txt'
        self.w2i = {}
        self.i2w = {}
        self.vocabulary_size = None
        self.findings = {}
        self.data = []

    def separate_each_finding(self):

        f = open(self.file_path)
        lines = f.readlines()

        cnt = 0
        finding = []

        for line in lines:
            lst = [i for i in line.split()]
            if lst[0] == 'finding':
                cnt += 1
                if cnt > 1:
                    self.findings[cnt-1] = finding
                    finding = []
                #########################
                if cnt == 3:
                    break
                #########################
            else:
                finding.append(list(l for l in line.split()))

    def word2id(self):

        ID = 1

        for key in self.findings:
            finding = self.findings[key]
            for j in range(len(finding)):
                if 'Token' in finding[j][0]:
                    word = finding[j][1][6:-2]
                    if self.w2i.get(word) == None:
                        self.w2i[word] = ID
                        ID += 1
        
        self.w2i['unknown_word'] = ID
        self.w2i['root_id'] = ID + 1
        self.i2w = {i: w for w, i in self.w2i.items()}

        self.vocabulary_size = len(self.w2i)
    
    def word2vec(self,word):

        ID = self.w2i[word]
        vec = [0 for _ in range(self.vocabulary_size)]
        vec[ID] = 1

        return vec
    
    def finding2vec(self):

        vec = []
        f_vec = []
        sent = []

        for key in self.findings:
            print(key)

            finding = self.findings[key]
            stored = 0

            for i in range(len(finding)):

                print('finding[i]:',finding[i])

                if 'sentence' in finding[i][0]:

                    if sent != []:
                        stored = i
                        f_vec.append(sent)
                        sent = []

                elif 'Token' in finding[i][0]:
                    index = int(finding[i][0][-2])
                    #print('index:',index)
                    pos = finding[i][3][5:-2]
                    #print('pos:',pos)
                    word = finding[i][1][6:-2]
                    #print('word:',word)
                    head = int(finding[i][4][5:-1])+stored
                    print('head:',head)
                    R = finding[i][5][8:-2]
                    #print('R:',R)

                    '''
                    if head != 0:
                        print('head:',finding[head])
                        print('head pos:',finding[head][3])
                        print('head pos head:',finding[head][3][5])
                    '''

                    if pos == 'NN':
                        ID = self.w2i[word]
                        if 'sentence' in finding[head][0]:
                            with_id = self.w2i['root_id']
                        else:                           
                            with_id = self.w2i[finding[head][1][6:-2]]
                        sent.append([ID,with_id,R]) 
                    else:
                        head = finding[head]
                        if head[0] != 'sentence':
                            if head[3][5:-2] == 'NN':
                                ID = self.w2i[word]
                                with_id = self.w2i[head[1][6:-2]]
                                sent.append([ID,with_id,R])
                            else:
                                pass
                        else:
                            pass

                elif i == len(finding) - 1:
                    f_vec.append(sent)
                    vec.append(f_vec)
                    f_vec = []

                else:
                    pass
        
        if f_vec != []:
            vec.append(f_vec)

        return vec

class MyDataset(torch.utils.data.Dataset):

    def __init__(self,data):
        self.data = data
        pass
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self,idx):
        pass

if __name__ == '__main__':

    v = Report2vec("IU_Xray")

    v.separate_each_finding()
    print(v.findings)
    v.word2id()
    cnt = 0
    for k in v.w2i:
        if cnt > 10:
            break
        print(v.w2i[k])
        cnt += 1
    vec = v.finding2vec()
    print(vec)
