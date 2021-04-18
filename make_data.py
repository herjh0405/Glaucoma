import pandas as pd
import os
import shutil

DataName = input("data = (ex. combine, pusan) ")
test_time = input('test_time = ')
eye = input("eye = (ex.OS, OD, None) ")
# eye = 'None'
inter = input("inter = (ex. interval 6 month = 180) ")



combine = pd.read_csv('./data/want_data.csv',index_col=0)
# pusan = pd.read_csv('./data/pusan.csv',index_col=0)


FileName = str(DataName) + str(test_time) + str(eye) + str(inter)  

if DataName == 'combine':
    csv = combine
else:
    csv = pusan    


if eye == 'OS':
    csv = csv[csv.Eye == eye]
elif eye == 'OD':
    csv = csv[csv.Eye == eye]
else:
    pass
    
csv = csv.reset_index(drop=True)    

def inter_idx(csvs,inters):
    data = csvs.copy()
    
    data = data.sort_values(by=['PID', 'Exam Date'], axis=0)
    data['Exam Date'] = pd.to_datetime(data['Exam Date'])
    
    idx = []
    for x in data['lid'].unique():
        temp = data[data['PID'] == x].copy()
        temp['Exam Date'] = (temp['Exam Date'] - temp['Exam Date'].iloc[0]).dt.days
        all_set = []
        for x in temp['Exam Date']:
            inter = [x]
            for y in temp['Exam Date']:
                if int(inters)-30 <= y-x <= int(inters)+30:
                    inter.append(y)
                    x = y
            all_set.append(inter)  
        for a in all_set:
            if len(a) == int(test_time):
                line = a
                idx += temp[temp['Exam Date'].isin(line) == True].index.tolist()
                break
            else:
                pass
    
    return idx

csv_idx = inter_idx(csv,inter)
csv = csv.iloc[csv_idx]


print(csv.shape)



def date2days(csvs):
    data = csvs.copy()
    
    data = data.sort_values(by=['lid', 'Exam Date'], axis=0)
    data['Exam Date'] = pd.to_datetime(data['Exam Date'])
    
    df_list = []
    for x in data['lid'].unique():
        temp = data[data['lid']==x].copy()
        temp['Exam Date'] = (temp['Exam Date'] - temp['Exam Date'].iloc[-2]).dt.days
        df_list.append(temp)
    
    return pd.concat(df_list)



new_file = date2days(csv)

print(len(csv['lid'].unique()))

new_file.to_csv(FileName + ".csv")
