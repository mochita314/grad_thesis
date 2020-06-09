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

    for i in range(1,3852):
        finding = sheet.cell(i,6).value
        with open(file_path,mode='a') as f:
            f.write('finding no.'+str(i))
            f.write('\n')
        sent_tokenize_list = sent_tokenize(finding)
        for j in range(len(sent_tokenize_list)):
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

parse_reports('/data/unagi0/kizawa/IU_X_ray/indiana_reports.xls','indiana_reports','data/med_parsed.txt')
