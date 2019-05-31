import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, flash, request, redirect

app = Flask(__name__)

################## Routes ######################
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process',methods=['POST'])
def process():
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']

    if name and age:
        return jsonify({'name':name,'age':age,'gender':gender})

    return jsonify({'error':'Missing data!'})

@app.route('/target',methods=['POST'])
def target():
    salary = float(request.form['salary'])
    contribution = float(request.form['contribution'])/100
    replacement_1 = float(request.form['replacement_1'])/100
    replacement_2 = float(request.form['replacement_2'])/100

    tax_rate = 0.2
    take_home_income = salary * (1 - contribution) * (1 - tax_rate)

    return jsonify({'target_0':take_home_income,'target_1':take_home_income * replacement_1,'target_2':take_home_income * replacement_2})



if __name__ == "__main__":
    app.run(debug=False)
