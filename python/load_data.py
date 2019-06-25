import os
import pandas as pd
import numpy as np


def load_glide_path(root_loc):
    file_loc = os.path.join(root_loc,'Glidepath.csv')
    dfGlidePath = pd.read_csv(file_loc).set_index('Age')

    return dfGlidePath

def load_model_portfolios(root_loc):
    file_loc = os.path.join(root_loc,'modelPortfolio.csv')
    dfModelPorts = pd.read_csv(file_loc)

    return dfModelPorts

def load_sim_runs(root_loc):
    root = os.path.join(root_loc,'Simulation_Returns')
    ddict = {}
    asset_class_names = []
    for file in os.listdir(root):
        name = os.path.splitext(file)[0]
        asset_class_names.append(name)
        ddict[name] = pd.read_csv(os.path.join(root, file),header = None)

    return ddict, asset_class_names

