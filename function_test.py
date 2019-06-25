import os
import pandas as pd
import numpy as np
import json
from python.load_data import load_glide_path, load_model_portfolios, load_sim_runs
# from python.calc_tax import calc_income_tax_liability, calc_fica_tax_liability, calc_take_home_income
from python.get_forecast_projection_new import get_forecast_projection

root_loc = 'data'
#######################
# Tax Input
#######################
fica_loc = os.path.join(root_loc,'fica_tax.json')
income_tax_loc = os.path.join(root_loc,'income_tax.json')

fica_dict = json.loads(open(fica_loc).read())
income_tax_dict = json.loads(open(income_tax_loc).read())
#######################
# Other Configs
#######################
dfGlidePath = load_glide_path(root_loc)
dfModelPorts = load_model_portfolios(root_loc)
DFs_asset_class_sim_run, asset_class_sim_run_ordering = load_sim_runs(root_loc)

mp_asset_class_column_ordering = ['Commodities','Global ex-US REIT','US REIT','Emerging Markets Equity','Developed Markets Large Cap',
                              'US Small Cap Growth','US Small Cap Value','US Large Cap Growth','US Large Cap Value',
                              'Global ex-US Small Cap','Emerging Markets Bond','Developed Markets Bond','US High Yield Bond',
                              'US Treasury Bond - 5 Plus Years','US Treasury Bond - 1 to 5 Years','US Corporate Bond',
                              'US Agency Bond','US Mortgage Backed Bond','US Municipal Bond','TIPS','Short-Term']
config = {}
config['glidepath'] = dfGlidePath
config['modelportfolios'] = dfModelPorts
config['simulation_returns'] = DFs_asset_class_sim_run
config['asset_class_order'] = mp_asset_class_column_ordering
config['income_tax'] = income_tax_dict
config['fica_tax'] = fica_dict
#######################
# Forecast Config
#######################
forecast_config = {}
forecast_config['percentiles'] = [0.3,0.5,0.7]
#######################
# Profile Function
#######################
profile = {}
profile['name'] = 'Spencer'
profile['gender'] = 'Male'
profile['age'] = 30
profile['salary'] = 100000
profile['retirement_age'] = 65
profile['account'] = {}
profile['account']['balance'] = 5000
profile['account']['contribution'] = 0.06
profile['account']['type'] = 'Traditional'
profile['social_security'] = {}
profile['social_security']['claim_age'] = 67
profile['social_security']['benefit'] = 32000
profile['annuity'] = {}
profile['annuity']['start_age'] = 70
profile['annuity']['benefit'] = 10000
# Assign spend down age
profile['spend_down_age'] = 92
# Assign target information
profile['target'] = {}
profile['target']['fixed'] = 80000


print(get_forecast_projection(profile, config, forecast_config))
