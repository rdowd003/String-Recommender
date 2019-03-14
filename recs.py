#String Recommender

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches


df = pd.read_csv('tennis_strings.csv')

df.drop(columns=['avg_trans_force','gauce_ac'],inplace=True) #too many NaNs
df['material'].fillna('unknown',inplace=True) #for now
df.fillna(round(df.mean(),1),inplace=True) #only a few (~18)

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

def remove_parenth_gauge(x):
    lst = list(x.split(' '))
    if lst[-1][0] == '(' and lst[-1][-1] == ')':
        return ' '.join(lst[0:-1])

def calculate_similarity(data_items):
    """Calculate the column-wise cosine similarity for a sparse
    matrix. Return a new dataframe matrix with similarities.
    """
    data_sparse = csr_matrix(data_items)
    similarities = cosine_similarity(data_sparse)
    sim = pd.DataFrame(data=similarities, index= data_items.index, columns= data_items.index)
    return sim

def return_last_item(x):
    last = x.split(' ')[-1]
    return last

ends = ['16', '17', '18', '16L', '(1.30)', '(1.35)', '17/1.25', '(1.20)',
       '15L', '(1.25)', '(1.28)', '(1.23)', '(1.32)',
       '(1.24)', '(1.31)', '1.27', '(1.21)', '(1.22)',
       '(1.26)', '(1.19)', '(1.18)', '(1.40)', '(1.27)', '(1.29)',
       '(1.38)', '(1.17)', '(1.15)', '(1.12)', '16/1.30', '15', '1.30',
       '1.20', '(1.275)', '1.25', '16L/1.25', '17/1.20',
       '125/16L', '18/1.20', '127/16', '130/16', '(1.10)', '125/16',
       '1.25/16L', '16/1.27', '3D', '17L', '1.35', '1.28',
       '(1.16)', '(1.05)', '17/1.24', '1.22', '1.33',
       '120', '15L-16']


def remove_string_end(x):
    splits = x.split(' ')
    if splits[-1] in ends:
        return ' '.join(splits[0:-1])
    else:
        return x

#Swing-speed dummy codes
d1 = {'Fast':3,'Medium':2,'Slow':1}

#Gauge-fixing
d2 = {0.:1.25,1.25:1.25}
d2b = {0.:1.25}
d3 = {0.:1.3}

#Dummy codes for material
d4 = {'Polyester':1, 'Nylon':2, 'Nylon/Zyex':3, 'Nylon/Polyurethane':4,
       'Nylon/Polyester':5, 'Gut':6,'Polyolefin':7,
       'Nylon/Polyolefin':8,'unknown':9}


#Original Dataframe for lookup dictionaries and recommendations
original = df.copy()
original['brand'] = get_brand(original.string)
original['brand'] = original.brand.str.replace('[^a-zA-Z]', '')
original['brand'] = original['brand'].map(lambda x: x.lower()) #lower for better matching
original['string'] = original['string'].map(lambda x: remove_string_end(x))
original['model'] = original['string'].map(lambda x: x.split(' ',1)[1])


#Remap swing-speed with dummy codes
df['swing_speed']=df['swing_speed'].map(d1)

### Eventually save data formatted after this part as new csv ###
#Change gauge's that are 1. and 0. to appropriate gauge's
df['gauge_nom'] = gauge_ones(df['gauge_nom'])
df['gauge_nom'] = np.where(df['string']=='Diadem Solstice Pro 16L (1.25)',df['gauge_nom'].map(d2),df['gauge_nom'])
df['gauge_nom'] = np.where(df['string']=='Double AR Twice Shark (1.25)',df['gauge_nom'].map(d2b),df['gauge_nom'])
df['gauge_nom'] = np.where(df['string']=='Tecnifibre HDX Tour 16 (1.30)',df['gauge_nom'].map(d3),df['gauge_nom'])


df['material'] = df['material'].map(d4)
df['string'] = df['string'].map(lambda x: x.split(' ',1)[1])
df['string'] = df['string'].map(lambda x: x.lower()) #.lower() for better matches later


#Remove string name and string code to isolate numeric-only feature matrix
strings = df.pop('string')
codes = df.pop('string_code')
strings = strings.values
codes = codes.values

#String names are NOT unique. Must attach code to make them unique
strings_unique = [m+' '+str(n) for m,n in zip(strings,codes)]

# Look up dictionaries
d5 = dict(zip(strings_unique,codes)) #string:code
d6 = dict((y,x) for x,y in d5.items()) #code:string
d7 = dict(zip(list(strings),strings_unique)) #unique_string_name:string_name
#print(df.head())


#Calculate similarity
sim_matrix = calculate_similarity(df)

#reattaching string codes (should not be part of similarity algorithms)
df['string_code'] = codes

'''
# For multiple recs
string_codes_for_rec = []
string_names = []
n = int(input('How many strings would you like recs for? Enter number (1+): '))
'''

# Get unique brands/strings for searching
brands = list(original.brand.unique())
string_list = list(strings)


#User input for string - user brand search if necessary
while True:
    try:
        n = input('How many string recommendations would you like to receive? Enter numeric value < 50: ')
        n = int(n)
        break
    except ValueError:
        print("No valid integer! Please try again: ")

yn = input('Do you know your string that you want recs for? Enter yes or no: ')


#Enter string directly
if yn == 'yes':
    user_string = input('What string do you currently use? Enter name and gauge (e.g.: Prince Lightning 16): ')
    user_brand = user_string.split(' ')[0]
    user_brand_guess = get_close_matches(user_brand.lower(),brands,1)[0]

#Search for brand and guess brand to find string
elif yn == 'no':
    user_brand = input('Enter brand to search for string: ')
    user_brand_guess = get_close_matches(user_brand.lower(),brands,1)[0]
    df_brand = original[['brand','model']][original['brand']==user_brand_guess]
    brand_strings = list(df_brand.model.unique())
    pd.options.display.max_rows = None
    print(brand_strings)
    user_string = input("which string?: ")
    user_string = user_brand_guess + ' ' + user_string


# Guess user string
user_string_guess = get_close_matches(user_string,string_list,n=1)[0]
user_string_guess_unique = d7[user_string_guess]
string_name = user_string_guess_unique.split(' ')[1] #string model name (from unique list)
s = int(user_string_guess_unique.split(' ')[-1]) #string index/look up code


#Gather recommendations from string code s
string_recs = sim_matrix.loc[s].nlargest(51)
string_recs = string_recs.index.tolist()

del string_recs[0] #number one will always be itself (s) - remove
names = []
for i in string_recs:
    names.append(d6[i])

#Remove strings that are exactly the same in name (duplicates)
for i,x in enumerate(names):
    if string_name in x:
        del names[i]

#Top ten (highest similiarty score)
names = pd.Series(names[:n])
names = names.map(d5)

original['brand'] = original['brand'].map(lambda x: x.capitalize())

#sort by index/code
recs_df = original[['brand','model','material','gauge_nom','spin_pot','energy_return']][df['string_code'].isin(names)]
recs_df.columns = ['Brand','Model','Material','Gauge','Spin Potential','Energy Return']
recs_df.sort_values(by='Brand')
print('')
print('Your string: ')
print(user_brand_guess.capitalize() + ' ' + user_string_guess.capitalize())
print('')
print('Your recommendations: ')
print(recs_df.head(n))











#
