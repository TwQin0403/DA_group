import glob
import os
import pandas as pd
import pdb

path = os.getcwd()
def df_covert(df):
    df = df[df['Shares']>0]
    df = df[[df.columns[1],df.columns[2]]]
    def search_last(cor_name):
        if cor_name[-4:] == 'CALL':
            return 'DROP'
        elif cor_name[-3:] == 'PUT':
            return 'DROP'
        else:
            return cor_name
    df[df.columns[0]]  = df[df.columns[0]].apply(search_last)
    df = df[df[df.columns[0]] != 'DROP']
    return df

result_list = []
for fname in glob.glob('{}/*.csv'.format(path)):
    df = pd.read_csv(fname)
    result = df_covert(df)
    name = fname.split('.')[0]
    result.to_csv('{}_rev.csv'.format(fname),index=None)

