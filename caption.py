# the code for proceccing reports
# got inspiration from 'Deep Fragment Embeddings for Bidrectional Image Sentence Mapping [Karpathy+ NeurIPS2014]'

import xlrd

def load_report(data_path):
    '''
    the function for loading report file
    '''

    report_data_file = xlrd.open_workbook(data_path)
    sheet = report_data_file.sheet_by_name('indiana_reports')
    reports_list = []

    for i in range(1,3852):
        finding = sheet.cell(i,6).value
        #if i>=3845:
            #print(finding)
            #print('\n')
        reports_list.append(finding)

    return reports_list

def make_dct():
    '''
    the function to make dictionary from the loaded reports
    '''
    return

lst = load_report('/data/unagi0/kizawa/IU_X_ray/indiana_reports.xls')