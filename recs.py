#String Recommender

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches


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

def get_brand(col):
    brand = col.map(lambda x: x.split(' ', 1)[0])
    return brand

def gauge_ones(col):
    temp = col.map(lambda x: 1.3 if x == 1.0 else x)
    return temp

#Original Dataframe for lookup dictionaries and recommendations
original = df.copy()
original['brand'] = get_brand(original.string)
original['model'] = original['string'].map(lambda x: x.split(' ',1)[1])

#Prepping numerical data (df) for algorithms
df.drop(columns=['avg_trans_force','gauce_ac'],inplace=True)
df['material'].fillna('unknown',inplace=True) #for now
df.fillna(df.mean(),inplace=True)

#Dummy codes for swing-speed
d1 = {'Fast':3,'Medium':2,'Slow':1}
df['swing_speed']=df['swing_speed'].map(d1)

#Change gauge's that are 1. and 0. to appropriate gauge's
df['gauge_nom'] = gauge_ones(df['gauge_nom'])
d2 = {0.:1.25,1.25:1.25}
d2b = {0.:1.25}
d3 = {0.:1.3}
df['gauge_nom'] = np.where(df['string']=='Diadem Solstice Pro 16L (1.25)',df['gauge_nom'].map(d2),df['gauge_nom'])
df['gauge_nom'] = np.where(df['string']=='Double AR Twice Shark (1.25)',df['gauge_nom'].map(d2b),df['gauge_nom'])
df['gauge_nom'] = np.where(df['string']=='Tecnifibre HDX Tour 16 (1.30)',df['gauge_nom'].map(d3),df['gauge_nom'])

#Dummy codes for material
d4 = {'Polyester':1, 'Nylon':2, 'Nylon/Zyex':3, 'Nylon/Polyurethane':4,
       'Nylon/Polyester':5, 'Gut':6,'Polyolefin':7,
       'Nylon/Polyolefin':8,'unknown':9}
df['material'] = df['material'].map(d4)

#Remove string name and string code to isolate numeric-only feature matrix
strings = df.pop('string')
codes = df.pop('string_code')
strings = strings.values
codes = codes.values

#Note: String names are NOT unique. Must add code to make unique
strings_unique = [m+' '+str(n) for m,n in zip(strings,codes)]

 #should not go in algorithm
d5 = dict(zip(strings_unique,codes)) #string:code
d6 = dict((y,x) for x,y in d5.items()) #code:string
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


string_codes_for_rec = []
string_names = []

#User input
n = int(input('How many strings would you like recs for? Enter number (1+): '))

yn = input('Do you know your string? Enter yes or no: ')
if yn == 'yes':
    user_string = input('What string do you currently use? Enter name and gauge (e.g.: Prince Lightning 16): ')
elif yn == 'no':
    user_brand = input('Enter brand to search: ')
    df_brand = original[['brand','model']][original['brand']==user_brand]

print(df_brand)
user_string = input("which string?: ")




string_list = list(strings)
user_string_guess = get_close_matches(user_string,string_list,n=1)[0]
string_name = user_string_guess.split(' ')[1] #string model name
s = int(user_string_guess.split(' ')[-1]) #string code



string_recs = sim_matrix.loc[s].nlargest(20)
string_recs = string_recs.index.tolist()
del string_recs[0] #number one will always be itself
names = []
for i in string_recs:
    names.append(d6[i])

#Remove strings that are exactly the same in name
for i,x in enumerate(names):
    if string_name in x:
        del names[i]

names = pd.Series(names[:11])
names = names.map(d5)

recs_df = original[['brand','model','material','gauge_nom','spin_pot','energy_return']][df['string_code'].isin(names)]
recs_df.sort_values(by='brand')
print('')
print('Your string: ')
print(user_string_guess)
print('')
print('Your recommendations: ')
print(recs_df.head(10))











#
