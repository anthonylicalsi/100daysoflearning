import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True,
                 'axes.titlepad': 20})

fig = plt.figure()
subplot = fig.add_subplot(1, 1, 1)
# file_name = 'C:\\anthony\\pandas-fundamentals\\artist_data.csv'
file_name = 'C:\\anthony\\pandas-fundamentals\\artwork_data.csv'
cols = ['id', 'accession_number', 'artist', 'artistRole', 'artistId', 'title',
        'dateText', 'medium', 'acquisitionYear']

df = pd.read_csv(file_name, usecols=cols)
acquisition_years = df.groupby('acquisitionYear').size()
acquisition_years.plot(ax=subplot, rot=45, logy=True, grid=True)
# plt.show()
# fig.show()
subplot.set_xlabel("Acquisition Year")
subplot.set_ylabel("Artworks Acquired")
subplot.locator_params(nbins=10, axis='x')
subplot.set_title("Tate Gallery Acquisitions")
plt.savefig('plot.png')
plt.show()

