import os
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP

#given inputs, we need to specify accumulation and spend down
#import the output from the load inputs functions
#import contributions, initial wealth, glide path

def load_ModelPortReturns():
    ModelPortReturnsBySimAndYear = np.load('../data/model_portfolio_output.npy')
    return ModelPortReturnsBySimAndYear

ModelPortReturnsBySimAndYear = load_ModelPortReturns()

def load_glide_path():
    dfGlidePath = pd.read_csv('../data/Glidepath.csv')
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

def forecast_accumulation_period(age, ret_age, equity_allocation_over_time, ctrbs, starting_wealths):
    no_sim_runs = 100
    accum_period = max(ret_age - age, 0)
    wealth_over_time = np.zeros((accum_period, no_sim_runs))
    if accum_period == 0:
        pass
    else:
        for n in range(accum_period):
            calculated_age = age + n
            m = lookup_closest_model_port(equity_allocation_over_time, n)
            for i in range(no_sim_runs):
                wealth_over_time[n][i] = accumulate(age = age, ret_age = ret_age, ctrbs = ctrbs, starting_wealth = starting_wealths,
                                                    sim_run = i, model_port = m, projection_year = n)

def accumulate(age, ret_age, ctrbs, starting_wealth, sim_run, model_port, projection_year):
    sim_run = i
    model_port = m
    projection_year = n
    MOY_wealth = starting_wealth * (1 + ModelPortReturnsBySimAndYear[m][i][n])
    EOY_wealth = MOY_wealth + ctrbs
    return ending_wealth


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
