import pandas as pd
import matplotlib.pyplot as plt


path_to_csv = input("Path to desired result.csv: ")
df = pd.read_excel(path_to_csv, index_col=0)

plt.imshow(df, cmap='hot', interpolation='nearest')

plt.show()