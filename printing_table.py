import pickle

finalTable = pickle.load(open("finalTable.pickle",'rb'))
i = 0;
while (i < len(finalTable)):
    print(finalTable[i])
    i += 1

