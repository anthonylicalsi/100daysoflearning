import pandas as pd
# import numpy as np

# file_name = 'C:\\anthony\\pandas-fundamentals\\artist_data.csv'
file_name = 'C:\\anthony\\pandas-fundamentals\\artwork_data.csv'

df = pd.read_csv(file_name)

print(df.size)
print(df.head)
print(df.columns)
print(df.loc[1035, 'artist'])
print(df.iloc[0:5, 0:5])

print('>>>>>>>>>>>>>>>')

small_df = df.iloc[49920:5019, :].copy()
grouped = small_df.groupby('artist')
print(type(grouped))


