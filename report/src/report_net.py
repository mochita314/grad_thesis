import torch
from torch.utils.data import DataLoader

from report_preprocess import *

class Report2vec:

    def __init__(self):

        self.file_path = 'data/med_parsed.txt'
        self.type_path = 'data/dependency_type.txt'
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
            else:
                finding.append(line)

    def word2id(self):

        id = 1

        for key in self.finding:
            finding = self.findings[key]
            for j in range(len(finding)):
                if 'Token' in finding[j]:
                    word = finding[j][1][6:-1]
                    if self.w2i.get(word) == None:
                        self.w2i[word] = id
                        id += 1
        
        self.w2i['unknown_word'] = id
        self.i2w = {i: w for w, i in self.w2i.items()}

        self.vocabulary_size = len(self.w2i)
    
    def word2vec(self,word):

        id = self.w2i[word]
        vec = [0 for _ in range(self.vocabulary_size)]
        vec[id] = 1

        return vec
    
    def finding2vec(self):

        for key in self.findings:
            finding = self.findings[key]
            for i in range(len(finding)):
                cnt = 0
                if 'sentence' in finding[i]:
                    cnt += 1
                    lst.append(finding[i])

                    


        return vec

class MyDataset(torch.utils.data.Dataset):

    def __init__(self,data):
        pass
    
    def __len__(self):
        pass
    
    def __getitem__(self,idx):
        pass

if __name__ == '__main__':

    #word_dct = load_obj('data/dct.pickle')
    #findings = separate_each_finding('data/med_parsed.txt')
    #save_obj(findings,'data/finding.pickle')