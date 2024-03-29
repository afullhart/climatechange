import numpy as np
import shutil
import os
baseDIR = '/content/drive/My Drive/Colab Notebooks'
inFOLDER = 'Script Input Files'
outFOLDER = 'Output_NEX_Ground_Precip_Diff'

if os.path.exists(os.path.join(baseDIR, outFOLDER)):
  shutil.rmtree(os.path.join(baseDIR, outFOLDER))
os.makedirs(os.path.join(baseDIR, outFOLDER))

usGRNDf = os.path.join(baseDIR, inFOLDER, 'USCLIGEN_Annual_Precip.csv')
#usGRNDf = os.path.join(baseDIR, inFOLDER, 'GHCNd_Annual_Precip.csv')
nexf = os.path.join(baseDIR, inFOLDER, 'NEX_USCLIGEN_Map_Sample_Annual_Precip.csv')
#nexf = os.path.join(baseDIR, inFOLDER, 'NEX_GHCNd_Map_Sample_Annual_Precip.csv')
outONEf = os.path.join(baseDIR, outFOLDER, 'NEX_Ground_Precip_Diff_Results.csv')
outTWOf = os.path.join(baseDIR, outFOLDER, 'NEX_Ground_Precip_Diff_Datapoints.csv')
outTHREEf = os.path.join(baseDIR, outFOLDER, 'bad.csv')

bad_list = []

stationID_list = []
us_dict = {}
print(usGRNDf)
with open(usGRNDf) as f:
  next(f)
  for line in f:
    row = line.strip('\n').split(',')
    stationID = row[0]
    if stationID[:2] in ['az', 'nv', 'nm', 'ut', 'US'] and stationID not in bad_list:
      stationID_list.append(row[0])
      us_dict[row[0]] = float(row[1])

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

results_dict = {}
datapts_dict = {md:{} for md in nex_dict}
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

for model in results_dict:
  y = np.array([float(datapts_dict[model][stn]) for stn in datapts_dict[model]])
  x = np.array([float(datapts_dict['obs'][stn]) for stn in datapts_dict['obs']])
  X = x[:,np.newaxis]
  a, b, c, d = np.linalg.lstsq(X, y)

  resid = []
  for i, x_val in enumerate(x):
    resid.append(abs(y[i] - a*x_val))
  resid_std = np.std(resid, ddof=1)

  resid_std_thresh = 999
  rmse = np.sqrt(np.mean([(y[i]-x[i])**2 for i, r in enumerate(resid) if r < resid_std_thresh*resid_std]))
  print(model)
  print(rmse)


with open(outONEf, 'w') as fo:
  fo.write('stationID,abspererr,rmse\n')
  for key in results_dict:
    fo.write(','.join([key, results_dict[key][0], results_dict[key][1]]) + '\n')

with open(outTWOf, 'w') as fo:
  fo.write('stationID,' + ','.join([key for key in datapts_dict]) + '\n')
  for stationID in datapts_dict['obs']:
    fo.write(stationID + ',' + ','.join([datapts_dict[key][stationID] for key in datapts_dict]) + '\n')

"""
with open(outTHREEf, 'w') as fo:
  badd = set(badd)
  print(len(badd))
  fo.write(','.join(badd))
"""
