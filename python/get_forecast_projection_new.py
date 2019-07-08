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
    retirement_age = profile['retirement_age']
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

    ## for 1/T* approach
    def calculate_conditional_life_estimate(profile, config):
        age = profile['age']
        gender = profile['gender']
        spend_down_age = profile['spend_down_age']
        dfMortTbl = config['mortality_table']
        percentile = 0.5 #static for now
        planning_horizon = spend_down_age - age + 1
        conditional_life_estimate_over_time = np.zeros(planning_horizon)

        ## Calculate the conditional life expectancy given each projected age
        for n in range(planning_horizon):
            starting_age = age + n
            SurvivalProbability = []
            tPx = 1
            for x in range(120-starting_age):
                tPx = tPx * (1 - dfMortTbl.Male[starting_age + x]) if gender == 'Male' else tPx * (1 - dfMortTbl.Female[starting_age + x])
                SurvivalProbability.append(tPx)
                    
            conditional_life_estimate_over_time[n]= starting_age + 1 + sum(1 for px in SurvivalProbability if px > percentile)

        return conditional_life_estimate_over_time

    # Spending curve boundary vectors
    spending_boundary_curve_vec = np.zeros(planning_horizon)
    a_param = 1/pow((spend_down_age-retirement_age)/2,2)
    a = (1 - profile['target']['minimum_ratio']) * a_param
    b = profile['target']['minimum_ratio']
    for n in range(len(spending_boundary_curve_vec)):
        if n + age >= retirement_age:
            spending_boundary_curve_vec[n] = a * pow((n + age - (spend_down_age+retirement_age)/2),2) + b

    # intialize 3 dynamic spending methods
    dynamic_spending_one_over_t_vec = np.zeros(planning_horizon)
    dynamic_spending_one_over_t_star_vec = np.zeros(planning_horizon)
    dynamic_spending_liability_ratio_vec = np.zeros(planning_horizon)
    dynamic_spending_methods_dictionary = {} #store all dynamic spending method vectors

    conditional_life_estimate_over_time = calculate_conditional_life_estimate(profile, config)
    
    for n in range(len(dynamic_spending_one_over_t_vec)):
        calculated_age = age + n    
        if calculated_age >= retirement_age:
            dynamic_spending_one_over_t_vec[n] = 1 / (spend_down_age + 1 - calculated_age)
            dynamic_spending_one_over_t_star_vec[n] = 1 / (min(conditional_life_estimate_over_time[n], spend_down_age + 1) - calculated_age)
            dynamic_spending_liability_ratio_vec[n] = spending_boundary_curve_vec[n] / np.sum(spending_boundary_curve_vec[n:])
        
    
    dynamic_spending_methods_dictionary['1/T'] = dynamic_spending_one_over_t_vec
    dynamic_spending_methods_dictionary['1/T*'] = dynamic_spending_one_over_t_star_vec
    dynamic_spending_methods_dictionary['Liability_Ratio'] = dynamic_spending_liability_ratio_vec

    return equity_allocation_over_time, beg_wealth_over_time, end_wealth_over_time, ss_income, annuity_income, spending_boundary_curve_vec, dynamic_spending_methods_dictionary

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
    
    return model_port_sim_run_output

def accumulate_for_one_year(age, ctrbs, starting_wealth, model_port, projection_year, config,num_sim_runs = 100):
    
    ModelPortReturnsBySimAndYear = calc_model_port_ret_across_sim_runs_at_projection_year(model_port, projection_year,config)

    EOY_wealth = np.zeros(num_sim_runs)

    for i in range(num_sim_runs):
            EOY_wealth[i] = starting_wealth[i] * (1 + ModelPortReturnsBySimAndYear[:,i]) + ctrbs

    return EOY_wealth

def decumulate_for_one_year(profile, starting_wealth, model_port, projection_year, SS_Income, annuity_Income, config,
                            spending_boundary_at_projection_year, dynamic_spending_ratio_at_projection_year, num_sim_runs = 100):
    
    ModelPortReturnsBySimAndYear = calc_model_port_ret_across_sim_runs_at_projection_year(model_port, projection_year,config)

    EOY_wealth = np.zeros(num_sim_runs)
    after_tax_retirement_income = np.zeros(num_sim_runs)
    income_tax_config = config['income_tax']

    ## Dynamic Spending function
    def determine_target_spending_at_node(profile, config, spending_boundary_at_projection_year, 
                                        dynamic_spending_ratio_at_projection_year,starting_wealth_at_sim_run,
                                        annuity_Income, SS_Income):
        # target = profile['target']['fixed']
        # income_tax_assumption = 0.25 #used to determine the after tax dynamic spending target at each node
        minimum_spending_boundary = profile['target']['essential']
        maximum_spending_boundary = profile['target']['discretional']
        minimum_boundary = minimum_spending_boundary * spending_boundary_at_projection_year #lower boundary
        maximum_boundary = maximum_spending_boundary * spending_boundary_at_projection_year #upper boundary

        ## Dynamic amount is the product of the starting account balance and the ratio following from the specified method
        # dynamic_amount = starting_wealth_at_sim_run * dynamic_spending_ratio_at_projection_year * (1 - income_tax_assumption) + annuity_Income + SS_Income if starting_wealth_at_sim_run > 0 else 0
        '''
        Apply tax model to accounts to calculate dynamical spending amount
        '''
        if profile['account']['type'] == 'Traditional': 
            dynamic_amount_tax = calc_income_tax_liability(starting_wealth_at_sim_run * dynamic_spending_ratio_at_projection_year, SS_Income, income_tax_config)
        else:
            dynamic_amount_tax = 0
        dynamic_amount = starting_wealth_at_sim_run * dynamic_spending_ratio_at_projection_year + annuity_Income + SS_Income - dynamic_amount_tax if starting_wealth_at_sim_run > 0 else 0
        
        ## Dynamic target is higher than lower boundary if enough account balance
        dynamic_target = max(minimum_boundary, min(maximum_boundary, dynamic_amount))

        return dynamic_target

    ## Define the optimization function 
    def objectiveFunction(pre_tax_withdrawal,target,accountType):
        if accountType == 'Traditional':
            income_tax_liability = calc_income_tax_liability(pre_tax_withdrawal, SS_Income, income_tax_config)
        else:
            income_tax_liability = 0
        return abs(pre_tax_withdrawal + SS_Income + annuity_Income - income_tax_liability - target)

    for i in range(num_sim_runs):
        target = determine_target_spending_at_node(profile, config, spending_boundary_at_projection_year, 
                                        dynamic_spending_ratio_at_projection_year, starting_wealth[i],
                                        annuity_Income, SS_Income)
        

        solution = minimize(fun=lambda x: objectiveFunction(x,target,profile['account']['type']), x0 = 0,method='SLSQP',bounds=[(0,starting_wealth[i])])
        optimized_pre_tax_withdrawal = solution.x
        EOY_wealth[i] = max(starting_wealth[i] - optimized_pre_tax_withdrawal,0) * (1 + ModelPortReturnsBySimAndYear[:,i])
        
        if profile['account']['type'] == 'Traditional':
            income_tax_liability = calc_income_tax_liability(optimized_pre_tax_withdrawal, SS_Income, income_tax_config)
        else:
            income_tax_liability = 0
        after_tax_retirement_income[i] = optimized_pre_tax_withdrawal + SS_Income + annuity_Income - income_tax_liability

    return EOY_wealth, after_tax_retirement_income

def lookup_closest_model_port(equity_allocation_over_time, projection_year):
    temp = round(equity_allocation_over_time[projection_year] * 100 / 0.01) * 0.01
    model_port = Decimal(temp).to_integral_value(rounding = ROUND_HALF_UP)
    return model_port

def calc_probability_of_ruin(profile, config, wealth_over_time, num_sim_runs=100):
    #mortality adjusted probability of ruin
    age = profile['age']
    retirement_age = profile['retirement_age']
    wealth_over_time_decumulation_only = wealth_over_time[retirement_age - age:,:]

    def calc_tPx(profile, config):
        dfMortTbl = config['mortality_table']
        gender = profile['gender']
        retirement_age = profile['retirement_age']

        #Calculate Survival Probability over Decumulation Period
        SurvivalProbability = []
        tPx = 1
        for x in range(120 - retirement_age):
            if gender == 'Male':
                tPx = tPx * (1 - dfMortTbl.Male[x + retirement_age])
            else:
                tPx = tPx * (1 - dfMortTbl.Female[x + retirement_age])
            
            SurvivalProbability.append(tPx)
        
        return SurvivalProbability
    
    SurvivalProbability = calc_tPx(profile, config)
    
    ## for each sim run, determine where wealth went to zero and calculate mortality adjusted probability of ruin
    ProbabilityOfRuinVector = []
    for i in range(num_sim_runs):
        temp = np.where(wealth_over_time_decumulation_only[:,i] < 100)
        if any(map(len,temp)):
            year_ran_out_money = temp[0][0]
            ProbabilityOfRuinVector.append(SurvivalProbability[year_ran_out_money])
        else:
            ProbabilityOfRuinVector.append(0)
    
    ProbabilityOfRuin = sum(ProbabilityOfRuinVector)/num_sim_runs
    
    return ProbabilityOfRuin

## Aggregate all the previous function before
def get_forecast_projection(profile, config, forecast_config, num_sim_runs=100):
    
    #calculate initial array and intermediate output
    equity_allocation_over_time, beg_wealth_over_time, end_wealth_over_time, ss_income, annuity_income, spending_boundary_curve_vec, dynamic_spending_methods_dictionary = initalize_arrays(profile, config, num_sim_runs)

    age = profile['age']
    spend_down_age = profile['spend_down_age']
    retirement_age = profile['retirement_age']
    planning_horizon = spend_down_age - age + 1
    ctrbs = profile['account']['contribution'] * profile['salary']
    percentiles = forecast_config['percentiles']
    essential_target = profile['target']['essential']
    discretional_target = profile['target']['discretional']
    dynamic_spending_method = str(profile['spending_strategy'])
    # dynamic_spending_method = str(config['dynamic_spending_method'])
    spending_curve_vec = dynamic_spending_methods_dictionary[dynamic_spending_method]

    age_vec = list(range(age,(spend_down_age+1)))

    #initialize income over time array
    income_over_time = np.zeros((planning_horizon, num_sim_runs))
        
    #Forecast Accumulation and Decumulation period
    for n in range(planning_horizon):
        calculated_age = age + n
        model_port = lookup_closest_model_port(equity_allocation_over_time, n)

        if calculated_age < retirement_age:
            end_wealth_over_time[n][:] = accumulate_for_one_year(age = calculated_age, ctrbs = ctrbs, starting_wealth = beg_wealth_over_time[n][:],
                                                        model_port = model_port, projection_year = n,
                                                        config=config, num_sim_runs = num_sim_runs)
        else:
            end_wealth_over_time[n][:],income_over_time[n][:] = decumulate_for_one_year(profile = profile, starting_wealth = beg_wealth_over_time[n][:],
                                                         model_port = model_port, projection_year = n,
                                                         SS_Income = ss_income[n], annuity_Income = annuity_income[n], 
                                                         config=config, spending_boundary_at_projection_year = spending_boundary_curve_vec[n], 
                                                         dynamic_spending_ratio_at_projection_year = spending_curve_vec[n], num_sim_runs = num_sim_runs)
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


    RuinProbability = calc_probability_of_ruin(profile, config, end_wealth_over_time, num_sim_runs=100)

    output_dictionary = {"Heuristics" : {"Ruin_Probability": RuinProbability},
                        "Income": income_output_list,
                        "Wealth": wealth_output_list,
                        "Age":age_vec,
                        "target_upperBound":list(discretional_target*spending_boundary_curve_vec),
                        "target_lowerBound":list(essential_target*spending_boundary_curve_vec),
                        "profile":{"income_start_index":max(retirement_age-age,0)},
                        "spending_strategy":profile['spending_strategy']}

    return output_dictionary  