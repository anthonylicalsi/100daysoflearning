# Load the Pandas libraries with alias 'pd'
import pandas as pd

# Read data from file 'filename.csv' in a Dataframe
file_name = 'C:\\anthony\\boreports\\GF_FAST6QA-2021-02-08-14-850.csv'
columns = ['Business Object ID', 'Business Object Type',
           'Date/Time of release/commit', 'Commit User', 'Commit Comment',
           'Business Object Modified By', 'Business Object Date Modified']
df = pd.read_csv(file_name, usecols=columns)

# Preview the first 5 lines of the loaded data
print(df.head())
print(df.size)
print(df.columns)

print(">>>>>>>>>>>>>>>>>>> result_df")
# result_df = data_frame[data_frame.notnull['Commit User']]
# result1 = df['Commit User'].notnull()
result1 = df.dropna(subset=['Commit User'])
print(result1.size)
print(result1.head())
result2 = result1.query('"Commit Comment" != ""')
