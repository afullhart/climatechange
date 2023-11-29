import numpy as np
import shutil
import os
baseDIR = '/content/drive/My Drive/Colab Notebooks'
inFOLDER = 'Script Input Files'
outFOLDER = 'Output_NEX_Ground_Precip_Diff'

if os.path.exists(os.path.join(baseDIR, outFOLDER)):
  shutil.rmtree(os.path.join(baseDIR, outFOLDER))
os.makedirs(os.path.join(baseDIR, outFOLDER))

#usGRNDf = os.path.join(baseDIR, inFOLDER, 'USCLIGEN_Annual_Precip.csv')
usGRNDf = os.path.join(baseDIR, inFOLDER, 'GHCNd_Annual_Precip.csv')
#nexf = os.path.join(baseDIR, inFOLDER, 'NEX_USCLIGEN_Map_Sample_Annual_Precip.csv')
nexf = os.path.join(baseDIR, inFOLDER, 'NEX_GHCNd_Map_Sample_Annual_Precip.csv')
outONEf = os.path.join(baseDIR, outFOLDER, 'NEX_Ground_Precip_Diff_Results.csv')
outTWOf = os.path.join(baseDIR, outFOLDER, 'NEX_Ground_Precip_Diff_Datapoints.csv')
outTHREEf = os.path.join(baseDIR, outFOLDER, 'bad.csv')

#Has missing NEX sample value
bad_list_one = ['az026132', 'USC00026132']
#Has suspect NEX sample value
bad_list_two = ['ut424856','ut428119','ut425182','ut423809','ut420061','ut420072','ut427598','ut429595','ut425186','ut422726','ut422057','ut422385','ut426919','ut421759','ut427271','ut426869','ut428733','ut424467','ut427846']
bad_list_three = ['USC00422726','USC00424856','USC00426919','USC00422057','USC00425186','USC00425194','USC00420819','USC00429346','USC00428973','USW00024127','USC00420061','USC00421590','USC00425892','USC00427165','USC00427846','USC00424467','USC00427271','USC00420820','USC00429595','USC00421759','USC00425826','USC00427064','USC00428828','USC00428119','USC00423809','USC00421446','USC00429165','USC00425182','USC00420072']
#Has suspect GHCNd sample value
bad_list_four = ['USC00027622', 'USC00025418']
bad_list = bad_list_one + bad_list_two + bad_list_three + bad_list_four

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
    #if est > 700.:
      #badd.append(stationID)
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




