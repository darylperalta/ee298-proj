import numpy as np
import pandas as pd
import seaborn
import matplotlib.pyplot as plt

df = pd.read_csv('../input/labels.csv')
freq = df['breed'].value_counts()

plt.figure()
freq_sorted = freq.sort_index()
seaborn.barplot(x=freq_sorted.index, y=freq_sorted)
plt.xticks(rotation=90)
plt.title('Breed Distribution')

plt.savefig("breed_dist.png")
