import nltk
from nltk.tokenize import sent_tokenize
from bllipparser import RerankingParser
import StanfordDependencies
import xlrd

nltk.download('punkt')

def parse_reports(data_path,sheet_name,file_path):
    '''
    '''
    report_data_file = xlrd.open_workbook(data_path)
    sheet = report_data_file.sheet_by_name(sheet_name)

    rrp = RerankingParser.fetch_and_load('GENIA+PubMed',verbose=True)
    sd = StanfordDependencies.get_instance(backend='subprocess')

    for i in range(910,3852):
        finding = sheet.cell(i,6).value
        with open(file_path,mode='a') as f:
            f.write('finding no.'+str(i))
            f.write('\n')
        sent_tokenize_list = sent_tokenize(finding)
        for j in range(len(sent_tokenize_list)):
            try:
                with open(file_path,mode='a') as f:
                    f.write('sentence no.'+str(j))
                    f.write('\n')
                sentence = sent_tokenize_list[j]
                tree = rrp.simple_parse(sentence)
                dependencies = sd.convert_tree(tree)
                for token in dependencies:
                    with open(file_path,mode='a') as f:
                        f.write(str(token))
                        f.write('\n')
            except:
                print('error!')
                with open(file_path,mode='a') as f:
                    f.write('error!!!')
                    f.write('\n')

def record_type(file_path,txt_path):

    type_dct = {}

    f = open(file_path)
    lines = f.readlines()

    #cnt = 0
    for line in lines:
        #cnt += 1
        #if cnt > 200:
            #break
        lst = [i for i in line.split()]
        for j in range(len(lst)):
            value = lst[j]
            if 'deprel=' in value:
                value = value[8:-2]
                if type_dct.get(value) == None:
                    type_dct[value] = 1
    
    with open(txt_path,mode='a') as f:
        for key in type_dct:
            f.write(str(key))
            f.write('\n')
                 
    return type_dct

def missing_record(file_path):

    f = open(file_path)
    lines = f.readlines()

    missing = []
    pre_lst = [0]

    for line in lines:
        lst = [i for i in line.split()]
        if lst[0] == 'finding':
            if pre_lst[0] == 'finding':
                num = int(pre_lst[1][3:])
                missing.append(num)
        pre_lst = lst

    return missing

if __name__ == '__main__':

    #parse_reports('/data/unagi0/kizawa/IU_X_ray/indiana_reports.xls','indiana_reports','data/med_parsed.txt')
    type_dct = record_type('data/med_parsed.txt','data/dependency_type.txt')
    missing = missing_record('data/med_parsed.txt')
    print(missing)