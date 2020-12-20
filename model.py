import numpy as np
import pandas as pd
from scipy import stats
import pickle
import warnings
warnings.filterwarnings('ignore')
from geopy.distance import geodesic
#importing data
df1=pd.read_csv("data/mer positions.csv")
df2=pd.read_excel("data/Data - Test technique PFE 8.xlsx")

#calculate the distance_mer column
def distance_mer (lat,long,mer_pos):
    distances=[geodesic((lat,long),(lat_m,long_m)).kilometers for lat_m,long_m in zip(mer_pos.latitude,mer_pos.longitude)]
    return min(distances)
df2['distance_mer']=[distance_mer(lat,long,df1) for lat,long in zip(df2.latitude,df2.longitude)]

df2=df2[['surface_reelle_bati','nombre_pieces_principales','distance_mer','prix']]
z = np.abs(stats.zscore(df2[['surface_reelle_bati','nombre_pieces_principales','distance_mer','prix']]))
df_o = df2[(z <2.9).all(axis=1)]
df_o["prix"] = np.log1p(df_o["prix"])
#model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
X=df_o.iloc[:,:3]
y = df_o.prix
model= LinearRegression()
model.fit(X,y)
#export the model
pickle.dump(model, open('model1.pkl','wb'))