import numpy as np

USCLIGENf = r'C:\Users\afullhart\Desktop\USCLIGEN_Annual_Precip.csv'
PRISMf = r'C:\Users\afullhart\Desktop\PRISM_USCLIGEN_Map_Sample_Annual_Precip.csv'


US_Dict = {}
with open(USCLIGENf) as f:
    next(f)
    for line in f:
        row = line.strip('\n').split(',')
        US_Dict[row[0]] = float(row[1])
        
PRISM_Dict = {}
with open(PRISMf) as f:
    next(f)
    for line in f:
        row = line.strip('\n').split(',')
        PRISM_Dict[row[0]] = float(row[1])/25.4
    
Results_Dict = {}
Absperror_List = []
for stationID in PRISM_Dict:
    if stationID[:2] in ['az', 'nv', 'nm', 'ut']:
        est = PRISM_Dict[stationID]
        obs = US_Dict[stationID]
        Absperror_List.append(abs(est-obs)/obs*100)
        print(str(est), str(obs), str(abs(est-obs)/obs*100))

avgperror = np.mean(Absperror_List)
medperror = np.median(Absperror_List)
print(avgperror)
print(medperror)

        
