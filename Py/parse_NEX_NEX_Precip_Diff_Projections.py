from prompt_toolkit.shortcuts.progress_bar.base import E
from google.colab import drive
drive.mount('/content/drive')

with open('/content/drive/My Drive/Colab Notebooks/in_percent_change_all_models.csv') as f:
  next(f)
  lines = f.readlines()

results_dict = {}
for line in lines:
  row = line.split('"')
  model = row[0].strip(',')
  avg_abs = [str(s) for s in eval(row[1])]
  avg_rel = [str(s) for s in eval(row[3])]
  results_dict[model] = [avg_abs, avg_rel]

keys = []
for key in results_dict:
  keys.append(key)
keys = sorted(keys, key=str.casefold)

with open('/content/drive/My Drive/Colab Notebooks/percent_change_all_models.csv', 'w') as fo:
  model_string = '_abs,'.join(keys) + '_abs,'
  fo.write(model_string)
  model_string = '_rel,'.join(keys) + '_rel\n'
  fo.write(model_string)
  for i in range(len(results_dict[keys[0]][0])):
    for j in range(2):
      for key in keys:
        fo.write(results_dict[key][j][i])
        
        if key != keys[-1]:
          fo.write(',')
        else:
          if j != 1:
            fo.write(',')
    fo.write('\n')
