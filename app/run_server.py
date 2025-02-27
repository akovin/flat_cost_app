import joblib
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from model.model import FeatureSelector, NumericPower, NumberSelector, OHEEncoder
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def start():

    data = pd.read_csv("app/data/data_moscow.csv",
                       names=['okrug', 'metro', 'distance_from_center', 'route_minutes', 'total_area', 'rooms', 'price'])

    if request.method == 'POST':
        okrug = request.form['okrug']
        metro = request.form['metro']
        minutes = int(request.form['route_minutes'])
        rooms = int(request.form['rooms'])
        total_area = int(request.form['total_area'])

        df = pd.DataFrame({'okrug': okrug,
                           'metro': metro,
                           'route_minutes': minutes,
                           'rooms': rooms,
                           'total_area': total_area}, index=[0])

        model = joblib.load('app/model/model_cat_boost.pkl')
        prediction = model.predict(df)
        prediction = round(prediction[0])
        return render_template("prediction.html", prediction=prediction)
    return render_template("index.html", okrugs=data.okrug.unique(), metros=data.metro.unique())


if __name__ == '__main__':
    app.run(debug=False)