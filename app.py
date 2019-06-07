import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, flash, request, redirect
from python.calc_spend_down_age import calc_spend_down_age
from python.calc_Social_Security import calc_social_security_benefit

app = Flask(__name__)

################## Routes ######################
@app.route('/')
def index():
    spend_down_age = calc_spend_down_age(30,'Male',0.7)
    ss_benefit = round(calc_social_security_benefit(100000,65))
    return render_template("index.html",spen_down_age = spend_down_age,ss_benefit=ss_benefit)

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

@app.route('/spenddown',methods=['POST'])
def spend_down():
    confidence_level = float(request.form['confidence_level'])/100
    gender = request.form['gender']
    age = int(request.form['age'])

    spend_down_age = calc_spend_down_age(age,gender,confidence_level)
    return jsonify({'spend_down_age':spend_down_age})

@app.route('/social_security',methods=['POST'])
def social_security():
    salary = float(request.form['salary'])
    claim_age = int(request.form['claim_age'])

    ss_benefit = round(calc_social_security_benefit(salary,claim_age))
    return jsonify({'social_security_benefit':ss_benefit})

if __name__ == "__main__":
    app.run(debug=False)
