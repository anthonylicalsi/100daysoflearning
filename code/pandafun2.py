import pandas as pd
import numpy as np

my_numpy_array = np.random.rand(3)
print(my_numpy_array)

my_series = pd.Series(my_numpy_array, index=["First", "Second", "Third"])
print(my_series)
print(my_series["First"])
print(my_series.index)

array_2d = np.random.rand(3, 2)
print(array_2d[0, 1])

df = pd.DataFrame(array_2d)
print(df)
print(df.columns)
df.columns = ["First", "Second"]
print(df)
print(df.columns)

print(df["Second"])
