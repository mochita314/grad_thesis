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

type_dct = record_type('data/med_parsed.txt','data/dependency_type.txt')