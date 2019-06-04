import os
import pandas as pd
import numpy as np

def calc_spend_down_age(age, gender, confidence_level):

    mortality_table = pd.read_csv('data/mortality.csv')

    return f'My age is {age} and my gender is {gender} and my confidence_level is {confidence_level}'
