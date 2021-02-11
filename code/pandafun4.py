import pandas as pd
# import numpy as np

# file_name = 'C:\\anthony\\pandas-fundamentals\\artist_data.csv'
file_name = 'C:\\anthony\\pandas-fundamentals\\artwork_data.csv'
cols = ['id', 'accession_number', 'artist', 'artistRole', 'artistId', 'title',
       'dateText', 'medium']

df = pd.read_csv(file_name, usecols=cols)
print(df.columns)
print(df.head)
print('>>>>>>>>>>>>>')
small_df = df.iloc[49920:50019, :].copy()
print(small_df.head)
print('>>>>>>>>>>>>>')
# small_df.to_excel('basic.xlsx', index=False)
small_df.to_json('default.json')
small_df.to_json('table.json', orient='table')
