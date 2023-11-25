import numpy as np

usCLIGENf = '/content/drive/My Drive/Colab Notebooks/USCLIGEN_Annual_Precip.csv'
nexf = '/content/drive/My Drive/Colab Notebooks/NEX_USCLIGEN_Map_Sample_Annual_Precip.csv'
outONEf = '/content/drive/My Drive/Colab Notebooks/NEX_Ground_Precip_Diff_Results.csv'
outTWOf = '/content/drive/My Drive/Colab Notebooks/NEX_Ground_Precip_Diff_Datapoints.csv'

stationID_list = []
us_dict = {}
with open(usCLIGENf) as f:
  next(f)
  for line in f:
    row = line.strip('\n').split(',')
    stationID = row[0]
    if stationID[:2] in ['az', 'nv', 'nm', 'ut'] and stationID != 'az026132':
      stationID_list.append(row[0])
      us_dict[row[0]] = float(row[1])*25.4

nex_dict = {}
with open(nexf) as f:
  next(f)
  for line in f:
    row = line.strip('\n').split(',')
    modelID = row[0]
    row = line.split(']","[')[0].split('"[')[1].split(',')
    stationIDs = [s.strip() for s in row]
    row = line.split(']","[')[1].strip(']"\n')
    datarow = [float(x) for x in row.split(',')]
    nex_dict[modelID] = {stationIDs[i]:datarow[i] for i, data in enumerate(datarow)}

#print(nex_dict['ACCESS1-0']['az026801'])
#print(nex_dict['ACCESS1-0']['az026132'])

results_dict = {}
datapts_dict = {md:{stationID:None for stationID in stationID_list} for md in nex_dict}
datapts_dict['obs'] = {stationID:str(us_dict[stationID]) for stationID in stationID_list}
for modelID in nex_dict:
  abspererr = []
  sqrerr = []
  for stationID in stationID_list:
    est = nex_dict[modelID][stationID]
    obs = us_dict[stationID]
    abspererr.append(abs(est-obs)/obs*100)
    sqrerr.append((est-obs)**2)
    datapts_dict[modelID][stationID] = str(est)
  results_dict[modelID] = [str(np.mean(abspererr)),
                           str(np.mean(sqrerr)**0.5)]

with open(outONEf, 'w') as fo:
  fo.write('stationID,abspererr,rmse\n')
  for key in results_dict:
    fo.write(','.join([key, results_dict[key][0], results_dict[key][1]]) + '\n')

with open(outTWOf, 'w') as fo:
  fo.write('stationID,' + ','.join([key for key in datapts_dict]) + '\n')
  for stationID in datapts_dict['obs']:
    fo.write(stationID + ',' + ','.join([datapts_dict[key][stationID] for key in datapts_dict]) + '\n')
    


