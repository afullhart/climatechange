import numpy as np

usCLIGENf = '/content/drive/My Drive/Colab Notebooks/USCLIGEN_Annual_Precip.csv'
nexf = '/content/drive/My Drive/Colab Notebooks/NEX_USCLIGEN_Map_Sample_Annual_Precip.csv'
outf = '/content/drive/My Drive/Colab Notebooks/NEX_Ground_Precip_Diff.csv'

us_dict = {}
with open(usCLIGENf) as f:
    next(f)
    for line in f:
        row = line.strip('\n').split(',')
        us_dict[row[0]] = float(row[1])

nex_dict = {}
with open(nexf) as f:
    next(f)
    for line in f:
        row = line.strip('\n').split(',')
        modelID = row[0]
        row = line.split(']","[')[0].split('"[')[1].split(',')
        stationID_list = [s.strip() for s in row]
        row = line.split(']","[')[1].strip(']"\n')
        datarow = [float(x)/25.4 for x in row.split(',')]
        nex_dict[modelID] = {stationID_list[i]:datarow[i] for i, data in enumerate(datarow)}

results_dict = {}
for modelID in nex_dict:
    print(modelID)
    abspererr = []
    sqrerr = []
    for stationID in stationID_list:
        if stationID[:2] in ['az', 'nv', 'nm', 'ut']:
            est = nex_dict[modelID][stationID]
            obs = us_dict[stationID]
            abspererr.append(abs(est-obs)/obs*100)
            sqrerr.append((est-obs)**2)

    results_dict[modelID] = [str(np.mean(abspererr)), 
                             str(np.mean(sqrerr)**0.5)]

with open(outf, 'w') as fo:
  fo.write('stationID,abspererr,rmse\n')
  for key in results_dict:
      fo.write(','.join([key, results_dict[key][0], results_dict[key][1]]) + '\n')

