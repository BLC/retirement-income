import os
import pandas as pd
import numpy as np

def get_advice_plan(profile,goal,config,forecast):
    return {'advice_1':f'Advice_1: Age is {profile["age"]} and Gender is {profile["gender"]}','advice_2':f'Advice_2: Age is {profile["age"]+30} and Name is {profile["name"]}',\
    'advice_3':f'Advice_3: Age is {profile["age"]+50} and Name is {profile["name"]}'}
