import pandas as pd
from os import walk
import csv

#find and parse filenames in dir
f = []
for (dirpath, dirnames, filenames) in walk('.\\bankfiles'):
    f.extend(filenames)
    break
uc = [x for x in f if x[:6] == 'CC_TXN'] 
ua = [x for x in f if x[:6] == 'ACC_TX'] 
sc = [x for x in f if x[:8] == 'CardTran']
sa = [x for x in f if x[:9] == 'AccountTr']
da = [x for x in f if x[-21:] == '.P000000011787830.csv' or x[-21:] == '.P000000020912573.csv']
dc = [x for x in f if x[:6] == 'DBS_CC']

#read existing db and find last extract date of each data source

df = pd.read_excel('.\\Financial Tracker - 2.0.xlsm', header=0)

df=df[['Acc','Date']]
df['Date']=pd.to_datetime(df['Date'])
a=df['Acc'].unique()
dflast=pd.DataFrame(columns=['Acc','Date'])

for x in a:
        y=df[df['Acc']==x]['Date'].max()
        dflast=pd.concat([dflast,pd.Series({'Acc':x,'Date':y}).to_frame().T],ignore_index=True)
dflast.set_index('Acc',inplace=True)


#Initialize a master dataframe to add data to
master=pd.DataFrame(columns=['Date','Transaction Description','Forex Amt','SGD Amt','Head','Acc'])

#Extract and transform data in Std Chrtd ccd files
for x in sc:
    print("reading file: ",x)
    df = pd.read_csv(".\\bankfiles\\"+x, header=2, skip_blank_lines=True)
    df.dropna(subset=['SGD Amount'],inplace=True)
    
    df2=pd.DataFrame()
    df2['Date'] = df['Date'].apply(lambda x: x.strip())
    df2['Date']=pd.to_datetime(df2['Date'], format="%d/%m/%Y")
    df2['Transaction Description']= df['DESCRIPTION']

    
    df2['Forex Amt']=df['Foreign Currency Amount'].fillna(value=0)
    df1=df['SGD Amount'].str.split(expand=True)
    df1[1]=pd.to_numeric(df1[1])
    df2['SGD Amt']= df1.apply(lambda x: x[1] if x[2]=="DR" else x[1]*-1 , axis=1)

    df2['Head']=""
    df2['Acc']="SC CCD " + pd.read_csv(".\\bankfiles\\"+x, header=0 ,nrows=0).columns[1][-4:] 
    master=pd.concat([master,df2[df2['Date']>dflast.loc[df2['Acc'][0],'Date']]], sort=False)

#Extract and transform data in Std Chrtd Acc files
for x in sa:
    print("reading file: ",x)
    df = pd.read_csv(".\\bankfiles\\"+x, header=3, skip_blank_lines=True, thousands=',')
    df['Deposit']=pd.to_numeric(df['Deposit'],errors='coerce').fillna(value=0)
    df['Withdrawal']=pd.to_numeric(df['Withdrawal'],errors='coerce').fillna(value=0)
  
	#df.dropna(subset=['SGD Amount'],inplace=True)

    df2=pd.DataFrame()
    df2['Date'] = df['\tDate'].apply(lambda x: x.strip())
    df2['Date']=pd.to_datetime(df2['Date'], format="%d/%m/%Y")
    df2['Transaction Description']= df['Transaction']

    
    #df2['Forex Amt']=df['Foreign Currency Amount'].fillna(value=0)
    df2['SGD Amt']= df['Withdrawal'] - df['Deposit']
    df2['Head']=""
    df2['Acc']="SC ACC " + pd.read_csv(".\\bankfiles\\"+x, header=2 ,nrows=0).columns[1][-4:] 

    master=pd.concat([master,df2[df2['Date']>dflast.loc[df2['Acc'][0],'Date']]], sort=False)

# extract and transform data in DBS bank acc files
for x in da:
    print("reading file: ",x)

    with open(".\\bankfiles\\"+x, newline='') as f:
        fp=f.readlines()
        #print(fp[17].split(",")[0])
        if fp[19].split(",")[0] == "Transaction Date": 
            acc_type="multiplier" 
        else: acc_type="savings"
    
    if acc_type=="savings":
        df = pd.read_csv(".\\bankfiles\\"+x, header=4, skip_blank_lines=True, sep=',',index_col=False)
        #print(df)
        df['Debit Amount']=pd.to_numeric(df['Debit Amount'],errors='coerce').fillna(value=0)
        df['Credit Amount']=pd.to_numeric(df['Credit Amount'],errors='coerce').fillna(value=0)
        df.fillna(value="",inplace=True)
        df2=pd.DataFrame()
        df2['Date']=pd.to_datetime(df['Transaction Date'])
        df2['Transaction Description']= df['Reference'].astype("string")+' '+ df['Transaction Ref1'].astype("string") +' ' + df['Transaction Ref2'].astype("string")+ ' ' + df['Transaction Ref3'].astype("string")
        df2['Forex Amt']= 0
        df2['SGD Amt']=df['Debit Amount']- df['Credit Amount']
        df2['Head']=""
        df2['Acc']="DBS BAC " + pd.read_csv(".\\bankfiles\\"+x, header=0 ,nrows=0).columns[1][-4:]
        #df2.head()
        master=pd.concat([master,df2[df2['Date']>dflast.loc[df2['Acc'][0],'Date']]], sort=False)
    
    if acc_type=="multiplier":
        df = pd.read_csv(".\\bankfiles\\"+x, header=5, skip_blank_lines=True, sep=',',index_col=False)
        #print(df)
        df['Debit Amount']=pd.to_numeric(df['Debit Amount'],errors='coerce').fillna(value=0)
        df['Credit Amount']=pd.to_numeric(df['Credit Amount'],errors='coerce').fillna(value=0)
        df.fillna(value="",inplace=True)
        df2=pd.DataFrame()
        df2['Date']=pd.to_datetime(df['Transaction Date'])
        df2['Transaction Description']= df['Statement Code'].astype("string")+' '+ df['Reference'].astype("string") +' ' + df['Client Reference'].astype("string") + ' ' + df['Additional Reference'].astype("string") + ' ' + df[' Misc Reference'].astype("string")
        df2['Forex Amt']= 0
        df2['SGD Amt']=df['Debit Amount']- df['Credit Amount']
        df2['Head']=""
        df2['Acc']="DBS BAC " + pd.read_csv(".\\bankfiles\\"+x, header=0 ,nrows=0).columns[1][-5:]
        #df2.head()
        master=pd.concat([master,df2[df2['Date']>dflast.loc[df2['Acc'][0],'Date']]], sort=False)

# Extract and transform data in UOB CCD files
for x in uc:
    print("reading file: ",x)
    df=pd.read_excel(".\\bankfiles\\"+x, header=9)
    df.dropna(subset=['Transaction Date'],inplace=True)
    df2=pd.DataFrame()
    df2['Date']=pd.to_datetime(df['Transaction Date'])
    df2['Transaction Description']=df['Description']
    df2['Forex Amt']=df['Foreign Currency Type'] + df['Transaction Amount(Foreign)'].map(str)
    df2['SGD Amt'] = df['Transaction Amount(Local)']
    df2['Head']=""
    
    label ="UOB CCD "+ pd.read_excel(".\\bankfiles\\"+x, header=4, nrows=0).columns[1][-4:]
    df2['Acc']=label
    master=pd.concat([master,df2[df2['Date']>dflast.loc[label,'Date']]], sort=False)

##Extract and Transform data in UOB Bank Acc files
for x in ua:
    print("reading file: ",x)
    df=pd.read_excel(".\\bankfiles\\"+x, header=7)
    df.dropna(subset=['Transaction Date'],inplace=True)
    df2=pd.DataFrame()
    df2['Date']=pd.to_datetime(df['Transaction Date'])
    df2['Transaction Description']=df['Transaction Description']
    df2['Forex Amt']=0
    df2['SGD Amt'] = df['Withdrawal']-df['Deposit']
    df2['Head']=""
    label="UOB BAC "+ pd.read_excel(".\\bankfiles\\"+x, header=4, nrows=0).columns[1][-4:]
    df2['Acc']=label
    master=pd.concat([master,df2[df2['Date']>dflast.loc[label,'Date']]], sort=False)


## Extract and Transform data in DBS bank scrape file
for x in dc:
    print("reading file: ",x)
    df=pd.read_csv(".\\bankfiles\\"+x, header=0)
    df2=pd.DataFrame()
    df2['Date']=pd.to_datetime(df['Transaction Date'])
    df2['Transaction Description']=df['Description']
    df2['Forex Amt']=0
    df2['SGD Amt'] = pd.to_numeric(df['Amount'].apply(lambda x: x[2:-2] if x[-2:]=='cr' else x[2:]))
    df2['Head']=""
    label="DBS CCD "+ x[-8:-4]
    df2['Acc']=label
    master=pd.concat([master,df2[df2['Date']>dflast.loc[label,'Date']]], sort=False)


# write data to master.csv
master.to_csv('masterETL.csv', index=False)


