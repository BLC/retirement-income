import os
import pandas as pd
import numpy as np
import json
from flask import Flask, jsonify, render_template, flash, request, redirect
from python.calc_spend_down_age import calc_spend_down_age
from python.calc_Social_Security import calc_social_security_benefit
from python.get_forecast_projection import get_forecast_projection
from python.get_advice_plan import get_advice_plan
from python.calc_tax import calc_income_tax_liability, calc_fica_tax_liability, calc_take_home_income

app = Flask(__name__)

################## Tax Configs ######################
fica_loc = os.path.join('data','fica_tax.json')
income_tax_loc = os.path.join('data','income_tax.json')

fica_config = json.loads(open(fica_loc).read())
income_tax_config = json.loads(open(income_tax_loc).read())
################## Routes ######################
@app.route('/')
def index():
    spend_down_age = calc_spend_down_age(30,'Male',0.7)
    ss_benefit = round(calc_social_security_benefit(100000,65))
    return render_template("index.html",spen_down_age = spend_down_age,ss_benefit=ss_benefit)

@app.route('/process',methods=['POST'])
def process():
    # Initialize the inputs
    profile = {}
    goal = {}
    config = []
    forecast = []
    # Assign basic profile information
    profile['name'] = request.form['name']
    profile['gender'] = request.form['gender']
    profile['age'] = int(request.form['age'])
    profile['salary'] = float(request.form['salary'])
    profile['retirement_age'] = int(request.form['retirement_age'])
    profile['account'] = {}
    profile['account']['balance'] = float(request.form['manageable_balance'])
    profile['account']['contribution'] = float(request.form['manageable_contrib'])
    profile['account']['type'] = request.form['manageable_tax']
    profile['social_security'] = {}
    profile['social_security']['claim_age'] = int(request.form['ss_claim_age'])
    profile['social_security']['benefit'] = float(request.form['ss_benefit'])
    profile['annuity'] = {}
    profile['annuity']['start_age'] = int(request.form['annuity_start_age'])
    profile['annuity']['benefit'] = float(request.form['annuity_benefit'])
    # Assign spend down age
    profile['spend_down_age'] = int(request.form['spend_down_age'])
    # Assign target information
    profile['target'] = {}
    profile['target']['essential'] = float(request.form['non_dis_target'])
    profile['target']['discretional'] = float(request.form['dis_target'])
    profile['target']['minimum_ratio'] = float(request.form['minimum_spending_ratio'])
    advice_result = get_advice_plan(profile,goal,config,forecast)
    return jsonify(profile)


@app.route('/target',methods=['POST'])
def target():
    salary = float(request.form['salary'])
    contribution = float(request.form['contribution'])/100
    tax_type = request.form['tax']
    if tax_type == 'Traditional':
        pre_tax_contrib = contribution
        post_tax_contrib = 0
    else:
        pre_tax_contrib = 0
        post_tax_contrib = contribution
    replacement_1 = float(request.form['replacement_1'])/100
    replacement_2 = float(request.form['replacement_2'])/100

    take_home_income = calc_take_home_income(salary,pre_tax_contrib,post_tax_contrib,income_tax_config,fica_config)
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
