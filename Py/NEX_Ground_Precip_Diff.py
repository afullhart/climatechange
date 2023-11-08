import numpy as np

USCLIGENf = r'C:\Users\afullhart\Desktop\USCLIGEN_Annual_Precip.csv'
NEXf = r'C:\Users\afullhart\Desktop\NEX_USCLIGEN_Map_Sample_Annual_Precip.csv'


US_Dict = {}
with open(USCLIGENf) as f:
    next(f)
    for line in f:
        row = line.strip('\n').split(',')
        US_Dict[row[0]] = float(row[1])

NEX_Dict = {}
with open(NEXf) as f:
    next(f)
    for line in f:
        row = line.strip('\n').split(',')
        modelID = row[0]
        row = line.split(']","[')[0].split('"[')[1].split(',')
        StationID_List = [s.strip() for s in row]
        row = line.split(']","[')[1].strip(']"\n')
        datarow = [float(x)/25.4 for x in row.split(',')]
        NEX_Dict[modelID] = {StationID_List[i]:datarow[i] for i, data in enumerate(datarow)}

Results_Dict = {}
for modelID in NEX_Dict:
    print(modelID)
    absperror = []
    for stationID in StationID_List:
        if stationID[:2] in ['az', 'nv', 'nm', 'ut']:
            est = NEX_Dict[modelID][stationID]
            obs = US_Dict[stationID]
            #absperror.append(abs(est-obs)/obs*100)
            absperror.append((est-obs)**2)
            print(str(est), str(obs), str(abs(est-obs)/obs*100))
    
    Results_Dict[modelID] = np.mean(absperror)**0.5
    #Results_Dict[modelID] = np.mean(absperror)
          
