import pandas as pd

df=pd.read_excel('placas.xlsx')

df.to_csv('placas2.csv', index = False)