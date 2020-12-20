from flask import Flask
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import pickle
from geopy.distance import geodesic
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
df2=pd.read_excel("data/Data - Test technique PFE 8.xlsx")
def distance_mer (lat,long,mer_pos):
    distances=[geodesic((lat,long),(lat_m,long_m)).kilometers for lat_m,long_m in zip(mer_pos.latitude,mer_pos.longitude)]
    return min(distances)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    lat=float(request.form['lat'])
    long = float(request.form['long'])
    nbr = float(request.form['nbr'])
    surf = float(request.form['surface'])
    dist_mer=distance_mer(lat,long,df2)
    print(dist_mer)
    prediction=model.predict([[surf,nbr,dist_mer]])
    output = int(np.expm1(prediction[0]))
    return render_template('index.html', prediction_text='The Price should be $ {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)