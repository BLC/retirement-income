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


if __name__ == "__main__":
    app.run(debug=False)
