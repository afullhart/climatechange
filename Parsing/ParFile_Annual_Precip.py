import os
import string


folder = r'C:\Users\afullhart\Downloads\2015parfiles\2015parfiles'
outfile = r'C:\Users\afullhart\Desktop\USCLIGEN_Annual_Precip.csv'
files = os.listdir( folder )
files = [f for f in files if f[:2] not in ['st', 'ak', 'hi', 'pi', 'pr', 'vi']]
files = [folder + '\\' + f for f in files]

ndays_months = [31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
with open(outfile, 'w') as fo:    
    
    fo.write( 'stationID,annualP\n' )
    
    for file in files:

        top_skip_lines = 3    
    
        all_lbl_chars = ((string.punctuation + string.ascii_letters)           \
                         .replace( '.', '' ))                                  \
                         .replace( '-', '' )

        with open(file) as fi:
            lines = fi.readlines()
    
        for i, line in enumerate(lines):

            for j, elem in enumerate(line):
                
                if elem in all_lbl_chars: 
                    label_end_i = j
                
                else:
                    pass

            label = line[:label_end_i+1]
            label = label.strip()

            dataline = line[8:]
            row = [dataline[k*6:k*6+6] for k in range(0,12)]

            if label == 'MEAN P':
                meanp_row = [float(dataline[k*6:k*6+6]) for k in range(0,12)]
            elif label == 'P(W/W)':
                pww_row = [float(dataline[k*6:k*6+6]) for k in range(0,12)]
            elif label == 'P(W/D)':
                pwd_row = [float(dataline[k*6:k*6+6]) for k in range(0,12)]
            else:
                pass
                
        annualP = sum([ndays_months[i]*meanp_row[i]*(pwd_row[i]/(1 - pww_row[i] + pwd_row[i])) for i in range(12)])
        print(annualP)           
        stationID = file.strip( '.par' ).split( '\\' )[-1]
        fo.write( stationID + ',' + str(annualP) + '\n' )
