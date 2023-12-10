import matplotlib.pyplot as plt
import pandas as pd
import scipy as scipy
import os

baseFOLDER = '/content/driver/My Drive/Colab Notebooks/Script Input Files'

precipEnsembleFILE = os.path.join(baseFOLDER, 'NEX_Ensemble_Stats_Precip.csv')
tmaxEnsembleFILE = os.path.join(baseFOLDER, 'NEX_Ensemble_Stats_MaxTemps.csv')
precipTseriesFILE = os.path.join(baseFOLDER, 'NEX_REGIONAL_PRECIP_PROJECTIONS.csv')
tmaxTseriesFILE = os.path.join(baseFOLDER, 'NEX_REGIONAL_TEMP_PROJECTIONS.csv')
precip1yrTseriesFILE = os.path.join(baseFOLDER, 'NEX_Regional_1Year_Precip_Tseries.csv')
tmax1yrTseriesFILE = os.path.join(baseFOLDER, 'NEX_Regional_1Year_MaxTemp_Tseries.csv')


fig, ax = plt.subplots(figsize=(15, 5))

df_tseries = pd.read_csv(precipTseriesFILE)
ccsm4_tseries = df_tseries['CCSM4_prcp']
canesm2_tseries = df_tseries['CanESM2_prcp']
miroc5_tseries = df_tseries['MIROC5_prcp']

df_ensemble = pd.read_csv(precipEnsembleFILE)
min_tseries = df_ensemble['min']
q25_tseries = df_ensemble['q25']
mean_tseries = df_ensemble['avg']
q75_tseries = df_ensemble['q75']
max_tseries = df_ensemble['max']

ax.plot(range(1985, 2071), min_tseries, linestyle='--', color='gray', linewidth=1, label='Ensemble Min/Max')
ax.plot(range(1985, 2071), mean_tseries, linestyle='--', color='black', linewidth=1, label='Ensemble Mean')
ax.fill_between(range(1985, 2071), q25_tseries, q75_tseries, linewidth=0, color='#272727', alpha=0.25, label='Ensemble Interquartile Range')
ax.plot(range(1985, 2071), max_tseries, linestyle='--', color='gray', linewidth=1)
ax.plot(range(1985, 2071), ccsm4_tseries, label='CCSM4')
ax.plot(range(1985, 2071), canesm2_tseries, label='CanESM2')
ax.plot(range(1985, 2071), miroc5_tseries, label='MIROC5')

ax.set_title('GCM Ensemble Statistics for Regional Annual Precip. (30-year Moving Avg.)', size=14)
ax.set_ylabel('Annual Precip. (mm)\n', size=12)
ax.set_xticks([1985, 2000, 2015, 2030, 2045, 2060, 2070])

# Shrink current axis's height by 15% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.15,
                 box.width, box.height * 0.85])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=6)

fig.show()



fig, ax = plt.subplots(figsize=(15, 5))

df_tseries = pd.read_csv(tmaxTseriesFILE)
ccsm4_tseries = df_tseries['CCSM4_tmx']
canesm2_tseries = df_tseries['CanESM2_tmx']
miroc5_tseries = df_tseries['MIROC5_tmx']

df_ensemble = pd.read_csv(tmaxEnsembleFILE)
min_tseries = df_ensemble['min']
q25_tseries = df_ensemble['q25']
mean_tseries = df_ensemble['avg']
q75_tseries = df_ensemble['q75']
max_tseries = df_ensemble['max']

ax.plot(range(1985, 2071), min_tseries, linestyle='--', color='gray', linewidth=1, label='Ensemble Min/Max')
ax.plot(range(1985, 2071), mean_tseries, linestyle='--', color='black', linewidth=1, label='Ensemble Mean')
ax.fill_between(range(1985, 2071), q25_tseries, q75_tseries, linewidth=0, color='#272727', alpha=0.25, label='Ensemble Interquartile Range')
ax.plot(range(1985, 2071), max_tseries, linestyle='--', color='gray', linewidth=1)
ax.plot(range(1985, 2071), ccsm4_tseries, label='CCSM4')
ax.plot(range(1985, 2071), canesm2_tseries, label='CanESM2')
ax.plot(range(1985, 2071), miroc5_tseries, label='MIROC5')

ax.set_title('GCM Ensemble Statistics for Regional Mean Daily High Temp. (30-year Moving Avg.)', size=14)
ax.set_ylabel('Mean Daily High Temp. (F)\n', size=12)
ax.set_xticks([1985, 2000, 2015, 2030, 2045, 2060, 2070])

# Shrink current axis's height by 15% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.15,
                 box.width, box.height * 0.85])

ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=6)

fig.show()



df_tseries = pd.read_csv(precip1yrTseriesFILE)
ccsm4_tseries = df_tseries['CCSM4']
df_tseries = pd.read_csv(precip1yrTseriesFILE)
canESM2_tseries = df_tseries['CanESM2']
df_tseries = pd.read_csv(precip1yrTseriesFILE)
miroc5_tseries = df_tseries['MIROC5']

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, figsize=(15, 5))
box = ax0.get_position()
ax0.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
box = ax1.get_position()
ax1.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
box = ax2.get_position()
ax2.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax0.set_title('Regional 1-year Annual Precip. (mm)')

ax0.plot([i for i, elem in enumerate(range(1985, 2100))], ccsm4_tseries, color='#1f77b4', label='CCSM4')
ax0.scatter([i for i, elem in enumerate(range(1985, 2100))], ccsm4_tseries, color='#1f77b4')
ax0.set_xticks([0, 15, 30, 45, 60, 75, 90, 105, 120])
ax0.set_xticklabels([1985, 2000, 2015, 2030, 2045, 2060, 2075, 2090, 2099])
y = np.array(ccsm4_tseries)
x = np.array([i for i, elem in enumerate(range(1985, 2100))])
res = scipy.stats.linregress(x, y, alternative='greater')
slope = res.slope
yint = res.intercept
ax0.plot([0, 120],[slope*0 + yint, slope*120 + yint], linestyle='--', color='black')
ax0.text(116, 400, 'slope\n{}mm/yr'.format(round(slope, 2)))

ax1.plot([i for i, elem in enumerate(range(1985, 2100))], canESM2_tseries, color='#ff7f0e', label='CanESM2')
ax1.scatter([i for i, elem in enumerate(range(1985, 2100))], canESM2_tseries, color='#ff7f0e')
ax1.set_xticks([0, 15, 30, 45, 60, 75, 90, 105, 120])
ax1.set_xticklabels([1985, 2000, 2015, 2030, 2045, 2060, 2075, 2090, 2099])
y = np.array(canESM2_tseries)
x = np.array([i for i, elem in enumerate(range(1985, 2100))])
res = scipy.stats.linregress(x, y, alternative='greater')
slope = res.slope
yint = res.intercept
ax1.plot([0, 120],[slope*0 + yint, slope*120 + yint], linestyle='--', color='black')
ax1.text(116, 400, 'slope\n{}mm/yr'.format(round(slope, 2)))

ax2.plot([i for i, elem in enumerate(range(1985, 2100))], miroc5_tseries, color='#2ca02c', label='MIROC5')
ax2.scatter([i for i, elem in enumerate(range(1985, 2100))], miroc5_tseries, color='#2ca02c')
ax2.set_xticks([0, 15, 30, 45, 60, 75, 90, 105, 120])
ax2.set_xticklabels([1985, 2000, 2015, 2030, 2045, 2060, 2075, 2090, 2099])
y = np.array(miroc5_tseries)
x = np.array([i for i, elem in enumerate(range(1985, 2100))])
res = scipy.stats.linregress(x, y, alternative='greater')
slope = res.slope
yint = res.intercept
ax2.plot([0, 120],[slope*0 + yint, slope*120 + yint], linestyle='--', color='black')
ax2.text(116, 385, 'slope\n{}mm/yr'.format(round(slope, 2)))

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05),
           fancybox=True, shadow=True, ncol=6)

fig.show()



df_tseries = pd.read_csv(tmax1yrTseriesFILE)
ccsm4_tseries = df_tseries['CCSM4']
df_tseries = pd.read_csv(tmax1yrTseriesFILE)
canESM2_tseries = df_tseries['CanESM2']
df_tseries = pd.read_csv(tmax1yrTseriesFILE)
miroc5_tseries = df_tseries['MIROC5']

fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, ncols=1, figsize=(15, 5))
box = ax0.get_position()
ax0.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
box = ax1.get_position()
ax1.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])
box = ax2.get_position()
ax2.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

ax0.set_title('Regional 1-year Mean Daily High Temp. (F)')

ax0.plot([i for i, elem in enumerate(range(1985, 2100))], ccsm4_tseries, color='#1f77b4', label='CCSM4')
ax0.scatter([i for i, elem in enumerate(range(1985, 2100))], ccsm4_tseries, color='#1f77b4')
ax0.set_xticks([0, 15, 30, 45, 60, 75, 90, 105, 120])
ax0.set_xticklabels([1985, 2000, 2015, 2030, 2045, 2060, 2075, 2090, 2099])
y = np.array(ccsm4_tseries)
x = np.array([i for i, elem in enumerate(range(1985, 2100))])
res = scipy.stats.linregress(x, y, alternative='greater')
slope = res.slope
yint = res.intercept
ax0.plot([0, 120],[slope*0 + yint, slope*120 + yint], linestyle='--', color='black')
ax0.text(116, 66, 'slope\n{}F/yr'.format(round(slope, 2)))

ax1.plot([i for i, elem in enumerate(range(1985, 2100))], canESM2_tseries, color='#ff7f0e', label='CanESM2')
ax1.scatter([i for i, elem in enumerate(range(1985, 2100))], canESM2_tseries, color='#ff7f0e')
ax1.set_xticks([0, 15, 30, 45, 60, 75, 90, 105, 120])
ax1.set_xticklabels([1985, 2000, 2015, 2030, 2045, 2060, 2075, 2090, 2099])
y = np.array(canESM2_tseries)
x = np.array([i for i, elem in enumerate(range(1985, 2100))])
res = scipy.stats.linregress(x, y, alternative='greater')
slope = res.slope
yint = res.intercept
ax1.plot([0, 120],[slope*0 + yint, slope*120 + yint], linestyle='--', color='black')
ax1.text(116, 66, 'slope\n{}F/yr'.format(round(slope, 2)))

ax2.plot([i for i, elem in enumerate(range(1985, 2100))], miroc5_tseries, color='#2ca02c', label='MIROC5')
ax2.scatter([i for i, elem in enumerate(range(1985, 2100))], miroc5_tseries, color='#2ca02c')
ax2.set_xticks([0, 15, 30, 45, 60, 75, 90, 105, 120])
ax2.set_xticklabels([1985, 2000, 2015, 2030, 2045, 2060, 2075, 2090, 2099])
y = np.array(miroc5_tseries)
x = np.array([i for i, elem in enumerate(range(1985, 2100))])
res = scipy.stats.linregress(x, y, alternative='greater')
slope = res.slope
yint = res.intercept
ax2.plot([0, 120],[slope*0 + yint, slope*120 + yint], linestyle='--', color='black')
ax2.text(116, 67, 'slope\n{}F/yr'.format(round(slope, 2)))


lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.05),
           fancybox=True, shadow=True, ncol=6)

fig.show()
