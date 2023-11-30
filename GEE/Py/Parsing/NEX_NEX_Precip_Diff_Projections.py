import os

fileDIR = '/content/drive/My Drive/GEE_Downloads'
parseFILE = '/content/drive/My Drive/Colab Notebooks/NEX_NEX_PRECIP_DIFF_PROJECTIONS_PARSED.csv'

files = os.listdir(fileDIR)

f = open(os.path.join(fileDIR, files[0]))
hdr_line = f.readline()
f.close()

lines = []
lines.append(hdr_line)
for afile in files:
  with open(os.path.join(fileDIR, afile)) as f:
    flines = f.readlines()
    for line in flines[1:]:
      lines.append(line)

results_dict = {}
for line in lines:
  row = line.split('"')
  model = row[0].strip(',')
  avg_prc = [str(s) for s in eval(row[1])]
  avg_abs = [str(s) for s in eval(row[3])]
  avg_rel = [str(s) for s in eval(row[5])]
  results_dict[model] = [avg_prc, avg_abs, avg_rel]

keys = []
for key in results_dict:
  keys.append(key)
keys = sorted(keys, key=str.casefold)

with open(parseFILE, 'w') as fo:
  model_string = '_prc,'.join(keys) + '_prc,'
  fo.write(model_string)
  model_string = '_abs,'.join(keys) + '_abs,'
  fo.write(model_string)
  model_string = '_rel,'.join(keys) + '_rel\n'
  fo.write(model_string)
  for i in range(len(results_dict[keys[0]][0])):
    for j in range(3):
      for key in keys:
        fo.write(results_dict[key][j][i])

        if key != keys[-1]:
          fo.write(',')
        else:
          if j != 2:
            fo.write(',')

    fo.write('\n')
