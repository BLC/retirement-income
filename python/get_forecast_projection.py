import os
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

test = False

def load_glide_path():
    if test == True:
        dfGlidePath = pd.read_csv('../data/Glidepath.csv')
    else:
        dfGlidePath = pd.read_csv('data/Glidepath.csv')
    #print(dfGlidePath.EquityLevel[5])
    return dfGlidePath

dfGlidePath = load_glide_path()

def determine_glide_path(spend_down_age, age):
    planning_horizon = spend_down_age - age
    equity_allocation_over_time = np.zeros((planning_horizon))
    for n in range(planning_horizon):
        equity_allocation_over_time[n] = dfGlidePath.EquityLevel[age + n]
    return equity_allocation_over_time

def lookup_closest_model_port(equity_allocation_over_time, projection_year):
    temp = round(equity_allocation_over_time[projection_year] * 100 / 0.01) * 0.01
    model_port = Decimal(temp).to_integral_value(rounding = ROUND_HALF_UP)
    return model_port

def load_model_portfolios():
    if test == True:
        dfModelPorts = pd.read_csv('../data/modelPortfolio.csv', header = None)
    else:
        dfModelPorts = pd.read_csv('data/modelPortfolio.csv', header = None)
    #print(dfModelPorts.iat[0,0])
    return dfModelPorts

dfModelPorts = load_model_portfolios()

def load_sim_runs():
    #Create dictionary of data frames for each asset class simulation return file
    #root = '../data/Simulation_Returns'
    if test == True:
        root = '../data/Simulation_Returns'
    else:
        root = 'data/Simulation_Returns'
    ddict = {}
    asset_class_names = []
    for file in os.listdir(root):
        name = os.path.splitext(file)[0]
        asset_class_names.append(name)
        ddict[name] = pd.read_csv(os.path.join(root, file),header = None)
    #print(ddict['Emerging Markets Bond'].iat[1,0])
    return ddict, asset_class_names

DFs_asset_class_sim_run, asset_class_sim_run_ordering = load_sim_runs()

#ordering in dfModelPorts
mp_asset_class_column_ordering = ['Commodities','Global ex-US REIT','US REIT','Emerging Markets Equity','Developed Markets Large Cap',
                              'US Small Cap Growth','US Small Cap Value','US Large Cap Growth','US Large Cap Value',
                              'Global ex-US Small Cap','Emerging Markets Bond','Developed Markets Bond','US High Yield Bond',
                              'US Treasury Bond - 5 Plus Years','US Treasury Bond - 1 to 5 Years','US Corporate Bond',
                              'US Agency Bond','US Mortgage Backed Bond','US Municipal Bond','TIPS','Short-Term']

def calc_model_port_ret_across_sim_runs_at_projection_year(model_port, projection_year, mp_asset_class_column_ordering, dfModelPorts, confidence_level):
    asset_class_sim_run_matrix = np.zeros((len(mp_asset_class_column_ordering), 100))
    projection_year = projection_year

    #Determine asset class sim run 21 x 100 matrix
    for i, name in enumerate(mp_asset_class_column_ordering):
        asset_class_sim_run_matrix[i][:] = DFs_asset_class_sim_run[name].iloc[:,projection_year]

    #Determine model_portfolio asset allocation weights 1 x 21 matrix
    model_port_asset_class_matrix = dfModelPorts.iloc[[model_port]]

    #Calculate model portfolio simulated output across all sim runs for specified projection year
    model_port_sim_run_output = np.matmul(model_port_asset_class_matrix, asset_class_sim_run_matrix)

    if test == True:
        pd.DataFrame(model_port_sim_run_output).to_csv('../data/test_model_portfolio_output.csv')

    #Select return at specified confidence level
    output_at_specified_percentile = np.percentile(model_port_sim_run_output,(1 - confidence_level)*100)

    return model_port_sim_run_output

calc_model_port_ret_across_sim_runs_at_projection_year(0, 1, mp_asset_class_column_ordering, dfModelPorts, confidence_level = 0.7)

num_model_ports = 100
num_sim_runs = 100
num_sim_years = 100

def accumulate(age, ret_age, ctrbs, starting_wealth, sim_run, model_port, projection_year):
    sim_run = i
    model_port = m
    projection_year = n
    #decide to either calculate wealth across all sim runs at once for a given model port and projection year
    ModelPortReturnsBySimAndYear = calc_model_port_ret_across_sim_runs_at_projection_year
    MOY_wealth = starting_wealth * (1 + ModelPortReturnsBySimAndYear)
    EOY_wealth = MOY_wealth + ctrbs
    return ending_wealth

def forecast_accumulation_period(age, ret_age, equity_allocation_over_time, ctrbs, starting_wealths):
    accum_period = max(ret_age - age, 0)
    wealth_over_time = np.zeros((accum_period, num_sim_runs))
    if accum_period == 0:
        pass
    else:
        for n in range(accum_period):
            calculated_age = age + n
            m = lookup_closest_model_port(equity_allocation_over_time, n)
            for i in range(num_sim_runs):
                wealth_over_time[n][i] = accumulate(age = age, ret_age = ret_age, ctrbs = ctrbs, starting_wealth = starting_wealths,
                                                    sim_run = i, model_port = m, projection_year = n)
    return 10

#get_tax_model()
## FICA tax and income tax with Social Security Benefit

#get the take home income

def pre_tax_to_post_tax(pre_tax_inflows, post_tax_inflows, social_security_inc):

    return 10

def optimize_withdrawal_ratio():
    #optimize the withdrawals from pre tax or post tax
    return 10

def cal_after_tax_income():

    return 10

def get_forecast_projection(profile,goal,config,forecast):

    return 10

def adaptive_spending():
    return 10
