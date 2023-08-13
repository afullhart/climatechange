import os


###############################################################################
'MEANP'
###############################################################################


folder = r'C:\Users\afullhart\Downloads\2015parfiles\2015parfiles'
outfolder = r'C:\Users\afullhart\Desktop\Climate Change\CLIGEN Network XYZ\MEANP'

files = [folder + '\\' + f for f in os.listdir(folder)]
files = [f for f in files if 'stations2015.txt' not in f]

data_dict = {}
for file in files:
    
    print(file)

    with open(file) as f:
        lines = f.readlines()

    xyline = lines[1]
    lat = float(xyline.split( 'LATT=' )[1].split( 'LONG=' )[0])
    lon = float(xyline.split( 'LONG=' )[1].split( 'YEARS=' )[0])
    xystr = str(lon) + ' ' + str(lat)
    
    line = lines[3]
    line_data = line[8:]
    data = [line_data[i*6:(i*6)+6].strip( '\n' ).lstrip().rstrip() for i in range(12)]
    data_dict[xystr] = data

for i in range(12):
    with open(outfolder + '\\' + 'MEANP_' + str(i+1) + '.txt', 'w') as fout:
        fout.write('x,y,data\n')
        for item in data_dict.items():
            x = item[0].split()[0]
            y = item[0].split()[1]
            data = item[1]
            fout.write( x + ',' + y + ',' + data[i] + '\n' )
            

###############################################################################
'SDEVP'
###############################################################################


folder = r'C:\Users\afullhart\Downloads\2015parfiles\2015parfiles'
outfolder = r'C:\Users\afullhart\Desktop\Climate Change\CLIGEN Network XYZ\SDEVP'

files = [folder + '\\' + f for f in os.listdir(folder)]
files = [f for f in files if 'stations2015.txt' not in f]

data_dict = {}
for file in files:
    
    print(file)

    with open(file) as f:
        lines = f.readlines()

    xyline = lines[1]
    lat = float(xyline.split( 'LATT=' )[1].split( 'LONG=' )[0])
    lon = float(xyline.split( 'LONG=' )[1].split( 'YEARS=' )[0])
    xystr = str(lon) + ' ' + str(lat)
    
    line = lines[4]
    line_data = line[8:]
    data = [line_data[i*6:(i*6)+6].strip( '\n' ).lstrip().rstrip() for i in range(12)]
    data_dict[xystr] = data

for i in range(12):
    with open(outfolder + '\\' + 'SDEVP_' + str(i+1) + '.txt', 'w') as fout:
        fout.write('x,y,data\n')
        for item in data_dict.items():
            x = item[0].split()[0]
            y = item[0].split()[1]
            data = item[1]
            fout.write( x + ',' + y + ',' + data[i] + '\n' )
            
            
###############################################################################
'SKEWP'
###############################################################################


folder = r'C:\Users\afullhart\Downloads\2015parfiles\2015parfiles'
outfolder = r'C:\Users\afullhart\Desktop\Climate Change\CLIGEN Network XYZ\SKEWP'

files = [folder + '\\' + f for f in os.listdir(folder)]
files = [f for f in files if 'stations2015.txt' not in f]

data_dict = {}
for file in files:
    
    print(file)

    with open(file) as f:
        lines = f.readlines()

    xyline = lines[1]
    lat = float(xyline.split( 'LATT=' )[1].split( 'LONG=' )[0])
    lon = float(xyline.split( 'LONG=' )[1].split( 'YEARS=' )[0])
    xystr = str(lon) + ' ' + str(lat)
    
    line = lines[5]
    line_data = line[8:]
    data = [line_data[i*6:(i*6)+6].strip( '\n' ).lstrip().rstrip() for i in range(12)]
    data_dict[xystr] = data

for i in range(12):
    with open(outfolder + '\\' + 'SKEWP_' + str(i+1) + '.txt', 'w') as fout:
        fout.write('x,y,data\n')
        for item in data_dict.items():
            x = item[0].split()[0]
            y = item[0].split()[1]
            data = item[1]
            fout.write( x + ',' + y + ',' + data[i] + '\n' )
      
            
###############################################################################
'MX5P'
###############################################################################


folder = r'C:\Users\afullhart\Downloads\2015parfiles\2015parfiles'
outfolder = r'C:\Users\afullhart\Desktop\Climate Change\CLIGEN Network XYZ\MX5P'

files = [folder + '\\' + f for f in os.listdir(folder)]
files = [f for f in files if 'stations2015.txt' not in f]

data_dict = {}
for file in files:
    
    print(file)

    with open(file) as f:
        lines = f.readlines()

    xyline = lines[1]
    lat = float(xyline.split( 'LATT=' )[1].split( 'LONG=' )[0])
    lon = float(xyline.split( 'LONG=' )[1].split( 'YEARS=' )[0])
    xystr = str(lon) + ' ' + str(lat)
    
    line = lines[14]
    line_data = line[8:]
    data = [line_data[i*6:(i*6)+6].strip( '\n' ).lstrip().rstrip() for i in range(12)]
    data_dict[xystr] = data

for i in range(12):
    with open(outfolder + '\\' + 'MX5P_' + str(i+1) + '.txt', 'w') as fout:
        fout.write('x,y,data\n')
        for item in data_dict.items():
            x = item[0].split()[0]
            y = item[0].split()[1]
            data = item[1]
            fout.write( x + ',' + y + ',' + data[i] + '\n' )


###############################################################################
'RATIO'
###############################################################################


folder = r'C:\Users\afullhart\Downloads\2015parfiles\2015parfiles'
outfolder = r'C:\Users\afullhart\Desktop\Climate Change\CLIGEN Network XYZ\RATIO'

files = [folder + '\\' + f for f in os.listdir(folder)]
files = [f for f in files if 'stations2015.txt' not in f]

data_dict = {}
for file in files:
    
    print(file)

    with open(file) as f:
        lines = f.readlines()

    xyline = lines[1]
    lat = float(xyline.split( 'LATT=' )[1].split( 'LONG=' )[0])
    lon = float(xyline.split( 'LONG=' )[1].split( 'YEARS=' )[0])
    xystr = str(lon) + ' ' + str(lat)
    
    pwwline = lines[6]
    pwdline = lines[7]
    pwwline_data = pwwline[8:]
    pwdline_data = pwdline[8:]
    
    pwwdata = [pwwline_data[i*6:(i*6)+6].strip( '\n' ).lstrip().rstrip() for i in range(12)]
    pwddata = [pwdline_data[i*6:(i*6)+6].strip( '\n' ).lstrip().rstrip() for i in range(12)]
    pwddata = [x if x != '.00' else '.01' for x in pwddata]
    
    data = [str(float(pwwdata[i])/float(pwddata[i])) for i, elem in enumerate(pwwdata)]
    
    data_dict[xystr] = data
    data_dict[xystr] = data

for i in range(12):
    with open(outfolder + '\\' + 'RATIO_' + str(i+1) + '.txt', 'w') as fout:
        fout.write('x,y,data\n')
        for item in data_dict.items():
            x = item[0].split()[0]
            y = item[0].split()[1]
            data = item[1]
            fout.write( x + ',' + y + ',' + data[i] + '\n' )
            

