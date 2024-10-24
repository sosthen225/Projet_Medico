from pprint import pprint

def data_organisees(data):
    data_organisees = {}

    maladies_cles = list(filter(lambda m: m.startswith('maladie'), data.keys()))
    traitements_cles = list(filter(lambda m: not m.startswith('maladie'), data.keys()))


    for maladie in maladies_cles:
        data_organisees[data[maladie][0]] = []

    for i in maladies_cles: 
        if not i[-1].isdigit(): # si la dernier lettre n'est pas un chiffre
            for j in traitements_cles:
                if '_' in j: # si element contient un _
                    splite = j.split('_')
                    if not splite[0][-1].isdigit():
                        data_organisees[data[i][0]].append(j)
                    
                elif not j[-1].isdigit():
                    data_organisees[data[i][0]].append(j)
        else:
            for j in traitements_cles:
                if '_' in j: # si element contient un _
                    splite = j.split('_')
                    if splite[0][-1].isdigit() and splite[0][-1] == i[-1]:
                        data_organisees[data[i][0]].append(j)
                    
                elif j[-1].isdigit() and j[-1] == i[-1]:
                    data_organisees[data[i][0]].append(j)
    return data_organisees