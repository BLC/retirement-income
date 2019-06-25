import os
import pandas as pd
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
from python.calc_tax import calc_income_tax_liability, calc_fica_tax_liability, calc_take_home_income
import json
from scipy.optimize import minimize

def initalize_arrays(profile, config,num_sim_runs = 100):

    initial_wealth = profile['account']['balance']
    age = profile['age']
    spend_down_age = profile['spend_down_age']
    planning_horizon = spend_down_age - age + 1
    annuity_start_age = profile['annuity']['start_age']
    annuity_benefit = profile['annuity']['benefit']
    ss_start_age = profile['social_security']['claim_age']
    ss_benefit = profile['social_security']['benefit']

    dfGlidePath = config['glidepath']

    #Initalize glide path
    equity_allocation_over_time = np.zeros(planning_horizon)
    for n in range(planning_horizon):
        equity_allocation_over_time[n] = dfGlidePath.EquityLevel[age + n]

    #define arrays of values that will vary over time
    beg_wealth_over_time = np.zeros((planning_horizon, num_sim_runs))
    end_wealth_over_time = np.zeros((planning_horizon,num_sim_runs))
    ss_income = np.zeros(planning_horizon)
    annuity_income = np.zeros(planning_horizon)

    #Set initial wealth at time 0
    for i in range(num_sim_runs):
        beg_wealth_over_time[0][i] = initial_wealth

    # SS benefit
    ss_income[ss_start_age - age: ] = ss_benefit
    annuity_income[annuity_start_age - age:] = annuity_benefit

    return equity_allocation_over_time, beg_wealth_over_time, end_wealth_over_time, ss_income, annuity_income


def calc_model_port_ret_across_sim_runs_at_projection_year(model_port_id,projection_year,config):

    mp_asset_class_column_ordering = config['asset_class_order']
    dfModelPorts = config['modelportfolios']
    DFs_asset_class_sim_run = config['simulation_returns']

    asset_class_sim_run_matrix = np.zeros((len(mp_asset_class_column_ordering), 100))

    #Determine asset class sim run 21 x 100 matrix
    for i, name in enumerate(mp_asset_class_column_ordering):
        asset_class_sim_run_matrix[i][:] = DFs_asset_class_sim_run[name].iloc[:,projection_year]

    #Determine model_portfolio asset allocation weights 1 x 21 matrix
    model_port_asset_class_matrix = dfModelPorts.iloc[[model_port_id]]

    #Calculate model portfolio simulated output across all sim runs for specified projection year
    model_port_sim_run_output = np.matmul(model_port_asset_class_matrix, asset_class_sim_run_matrix)
    
    # if test == True:
    #     pd.DataFrame(model_port_sim_run_output).to_csv('../data/test_model_portfolio_output.csv')
    return model_port_sim_run_output

def accumulate_for_one_year(age, ctrbs, starting_wealth, model_port, projection_year, config,num_sim_runs = 100):
    
    ModelPortReturnsBySimAndYear = calc_model_port_ret_across_sim_runs_at_projection_year(model_port, projection_year,config)

    EOY_wealth = np.zeros(num_sim_runs)

    for i in range(num_sim_runs):
            EOY_wealth[i] = starting_wealth[i] * (1 + ModelPortReturnsBySimAndYear[:,i]) + ctrbs

    return EOY_wealth

def decumulate_for_one_year(age, target, starting_wealth, model_port, projection_year, SS_Income, annuity_Income, config,num_sim_runs = 100):
    
    ModelPortReturnsBySimAndYear = calc_model_port_ret_across_sim_runs_at_projection_year(model_port, projection_year,config)

    EOY_wealth = np.zeros(num_sim_runs)
    after_tax_retirement_income = np.zeros(num_sim_runs)

    income_tax_config = config['income_tax']
    # Define the optimization function 
    def objectiveFunction(pre_tax_withdrawal):
        income_tax_liability = calc_income_tax_liability(pre_tax_withdrawal, SS_Income, income_tax_config)
        return abs(pre_tax_withdrawal + SS_Income + annuity_Income - income_tax_liability - target)

    for i in range(num_sim_runs):
        solution = minimize(fun=objectiveFunction, x0 = 0,method='SLSQP',bounds=[(0,starting_wealth[i])])
        optimized_pre_tax_withdrawal = solution.x
        EOY_wealth[i] = max(starting_wealth[i] - optimized_pre_tax_withdrawal,0) * (1 + ModelPortReturnsBySimAndYear[:,i])
        income_tax_liability = calc_income_tax_liability(optimized_pre_tax_withdrawal, SS_Income, income_tax_config)
        after_tax_retirement_income[i] = optimized_pre_tax_withdrawal + SS_Income + annuity_Income - income_tax_liability

    return EOY_wealth, after_tax_retirement_income


def lookup_closest_model_port(equity_allocation_over_time, projection_year):
    temp = round(equity_allocation_over_time[projection_year] * 100 / 0.01) * 0.01
    model_port = Decimal(temp).to_integral_value(rounding = ROUND_HALF_UP)
    return model_port

## Aggregate all the previous function before
def get_forecast_projection(profile, config, forecast_config, num_sim_runs=100):
    
    #calculate initial outputs
    equity_allocation_over_time, beg_wealth_over_time, end_wealth_over_time, ss_income, annuity_income = initalize_arrays(profile, config, num_sim_runs)

    age = profile['age']
    spend_down_age = profile['spend_down_age']
    retirement_age = profile['retirement_age']
    planning_horizon = spend_down_age - age + 1
    
    ctrbs = profile['account']['contribution'] * profile['salary']
    percentiles = forecast_config['percentiles']
    target = profile['target']['fixed']

    age_vec = list(range(age,(spend_down_age+1)))

    #initialize income over time array and objective function constraint
    income_over_time = np.zeros((planning_horizon, num_sim_runs))
    
    #Forecast Accumulation Perioß
    for n in range(planning_horizon):
        calculated_age = age + n
        model_port = lookup_closest_model_port(equity_allocation_over_time, n)

        if calculated_age < retirement_age:
            end_wealth_over_time[n][:] = accumulate_for_one_year(age = calculated_age, ctrbs = ctrbs, starting_wealth = beg_wealth_over_time[n][:],
                                                        model_port = model_port, projection_year = n,
                                                        config=config, num_sim_runs = num_sim_runs)
        else:
            end_wealth_over_time[n][:],income_over_time[n][:] = decumulate_for_one_year(age = calculated_age, target = target, starting_wealth = beg_wealth_over_time[n][:],
                                                         model_port = model_port, projection_year = n,
                                                         SS_Income = ss_income[n], annuity_Income = annuity_income[n], 
                                                         config=config, num_sim_runs = num_sim_runs)
        if n < planning_horizon - 1:
            beg_wealth_over_time[n+1][:] = end_wealth_over_time[n][:]


    #Nested Dictionary output
    income_output_list = []
    wealth_output_list = []

    for p in range(0, len(percentiles)):
        wealth_over_time_at_specified_percentile = np.zeros(planning_horizon)
        income_over_time_at_specified_percentile = np.zeros(planning_horizon)
        for n in range(planning_horizon):
            wealth_over_time_at_specified_percentile[n] = np.percentile(beg_wealth_over_time[n][:], percentiles[p])
            income_over_time_at_specified_percentile[n] = np.percentile(income_over_time[n][:], percentiles[p])
        income_output_list.append({'percentile':percentiles[p],'income':list(income_over_time_at_specified_percentile)})
        wealth_output_list.append({'percentile':percentiles[p],'wealth':list(wealth_over_time_at_specified_percentile)})

    output_dictionary = {"Heuristics" : {"Ruin_Probability": 0.3},
                        "Income": income_output_list,
                        "Wealth": wealth_output_list,
                        "Age":age_vec}

    return output_dictionary  