import os
import pandas as pd
import numpy as np
from flask import Flask, jsonify, render_template, flash, request, redirect

app = Flask(__name__)

################## Routes ######################
@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
