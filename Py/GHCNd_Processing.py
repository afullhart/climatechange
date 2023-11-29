import numpy as np
import requests

stationIDLINK = 'https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt'
metadataLINK = 'https://www.ncei.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt'

url = stationIDLINK
req = requests.get(url)
text = req.text

keepers_step_one = []
lines = (line for line in text.splitlines())
for line in lines:
  row = line.split()
  stationID = row[0]
  if stationID[:2] == 'US':
    state = row[4]
    if state in ['AZ', 'NM', 'NV', 'UT']:
      keepers_step_one.append(stationID)

url = metadataLINK
req = requests.get(url)
text = req.text

keepers_step_two = []
lines = (line for line in text.splitlines())
for line in lines:
  row = line.split()
  if 'PRCP' in row and row[0] in keepers_step_one:
    if int(row[4]) <= 1974 and int(row[5]) >= 2013:
      keepers_step_two.append(row[0])


from datetime import datetime as dt
from datetime import timedelta
import shutil
import os

dataLINK = 'https://www.ncei.noaa.gov/data/global-historical-climatology-network-daily/access'
baseDIR = '/content/drive/My Drive/Colab Notebooks'
outFOLDER = 'Output_GHCNd_Processing'
outf = os.path.join(baseDIR, outFOLDER, 'GHCNd_Processing_Results.csv')

if os.path.exists(os.path.join(baseDIR, outFOLDER)):
  shutil.rmtree(os.path.join(baseDIR, outFOLDER))
os.makedirs(os.path.join(baseDIR, outFOLDER))

dates = []
start_date = dt(1974, 1, 1, 0, 0)
end_date = dt(2013, 12, 31, 0, 0)
date = start_date
while date < end_date:
  dates.append(date)
  date = date + timedelta(days=1)

#No html address
bad = ['USC00428733', 'USC00027390', 'USC00265869', 'USC00027390', 'USC00299128', 'USC00422385', 'USC00426869', 'USW00023051']
keepers = keepers_step_two
keepers = [k for k in keepers if k not in bad]
data = []
for keeper in keepers:
  print(keeper)
  ct = 0
  url = dataLINK + '/' + keeper + '.csv'
  req = requests.get(url)
  text = req.text

  lines = [line for line in text.splitlines()]
  save_lines = []
  hdrs = lines[0].split(',')
  prcp_i = hdrs.index('"PRCP"')
  date_i = hdrs.index('"DATE"')
  for line in lines[1:]:
    row = line.split('","')
    name_no_comma = row[5].replace(',', '')
    line = line.replace(row[5], name_no_comma)
    line = line.replace('","', ',')
    row = line.split(',')
    date = dt.strptime(row[date_i].strip('"'), '%Y-%m-%d')
    prcp = row[prcp_i].strip('"')
    if date.year >= 1974 and date.year <= 2013:
      if prcp != '' and not any([s in prcp for s in ['P', 'T', '9999']]):        
        prcp = float(prcp)
        save_lines.append(prcp)  
      else:
        ct += 1

  if float(ct)/float(len(dates))*100. <= 5.:
    data.append([keeper.strip('.csv'), row[3], row[2], str(sum(save_lines)/40./10.)])

with open(outf, 'w') as fo:
  fo.write('stationID,x,y,prcp\n')
  for elem in data:
    fo.write(','.join([e for e in elem]) + '\n')


