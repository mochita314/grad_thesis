from report_preprocess import save_obj,load_obj

def separate_each_finding(file_path):

    f = open(file_path)
    lines = f.readlines()

    cnt = 0
    finding = []
    findings = {}

    for line in lines:
        lst = [i for i in line.split()]
        if lst[0] == 'finding':
            cnt += 1
            if cnt > 1:
                findings[cnt-1] = finding
                finding = []
        else:
            finding.append(line)
    
    return findings

def 


if __name__ == '__main__':

    word_dct = load_obj('data/dct.pickle')
    findings = separate_each_finding('data/med_parsed.txt')
    save_obj(findings,'data/finding.pickle')