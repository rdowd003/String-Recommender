#String Recommender

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv('tennis_strings.csv')

'''
#Visualize Nans in feature columns
sns.heatmap(df.isnull(),yticklabels=False,cbar=False,cmap='YlGnBu')
sns.set(rc={'figure.figsize':(10,10)})
plt.title("Plot of Null Values in Feature Columns (Null=Yellow)",fontsize=20)
plt.show()

nulls = df.isnull()
print(nulls.sum(axis=0))
'''

def get_brand_and_gauge(col):
    brand = col.map(lambda x: x.split(' ', 1)[0])
    gauge = col.map(lambda x: x.split(' ')[-1])
    return brand,gauge

#Original Dataframe for lookup dictionaries and recommendations
original = df.copy()
#gauge correction dictionary

d_gauge = {1.0:}
original['brand'] = get_brand_and_gauge(original.string)[0]
original['gauge'] = get_brand_and_gauge(original.string)[1]

#Cleaning data for algorithms
df.drop(columns=['avg_trans_force','gauce_ac'],inplace=True)
df['material'].fillna('unknown',inplace=True)
df.fillna(df.mean(),inplace=True)
d1 = {'Fast':3,'Medium':2,'Slow':1}
df['swing_speed']=df['swing_speed'].map(d1)
strings = df.pop('string')
codes = df.pop('string_code')
d2 = dict(zip(codes,strings))
d3 = {'Polyester':1, 'Nylon':2, 'Nylon/Zyex':3, 'Nylon/Polyurethane':4,
       'Nylon/Polyester':5, 'Gut':6,'Polyolefin':7,
       'Nylon/Polyolefin':8,'unknown':9}
df['material'] = df['material'].map(d3)






#print(df.head())


#Calculate similarity

def calculate_similarity(data_items):
    """Calculate the column-wise cosine similarity for a sparse
    matrix. Return a new dataframe matrix with similarities.
    """
    data_sparse = csr_matrix(data_items)
    similarities = cosine_similarity(data_sparse)
    sim = pd.DataFrame(data=similarities, index= data_items.index, columns= data_items.index)
    return sim

sim_matrix = calculate_similarity(df)
df['string_code'] = codes

#pick an index (string) to find n-similar items (strings) to
s = 35

string_recs = sim_matrix.loc[s].nlargest(10)
string_recs = string_recs.index.tolist()

recs = original['string'][df['string_code'].isin(string_recs)]
print(recs)







#
