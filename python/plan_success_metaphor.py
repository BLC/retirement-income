import numpy as np
from python.model_port_helper import calc_model_port_ret_across_sim_runs_at_projection_year, lookup_closest_model_port
from python.initialize import initalize_arrays

def calc_Ret_PVs(profile, config, projection_year, model_port, income_over_time, wealth_over_time, target_lower_bound, num_sim_runs=100):
    initial_vector = initalize_arrays(profile, config, num_sim_runs)
    equity_allocation_over_time = initial_vector['equity_allocation']

    age = profile['age']
    spend_down_age = profile['spend_down_age']
    retirement_age = profile['retirement_age']
    planning_horizon = spend_down_age - age + 1
    ctrbs = profile['account']['contribution'] * profile['salary']

    #Calculate discount factors
    def calc_disc_factors(config, planning_horizon, equity_allocation_over_time,num_sim_runs = 100):
        disc_factors = np.zeros((num_sim_runs,planning_horizon))
        for n in range(planning_horizon):
            model_port = lookup_closest_model_port(equity_allocation_over_time, n)
            for i in range(num_sim_runs):
                if n == 0:
                    disc_factors[i][n] = 1 / 1 (1 + calc_model_port_ret_across_sim_runs_at_projection_year(model_port, n,config))
                else:
                    disc_factors[i][n] = (1/ (1 + calc_model_port_ret_across_sim_runs_at_projection_year(model_port, n,config)) * disc_factors[i][n-1] 
        return disc_factors
    
    disc_factors = calc_disc_factors(config, planning_horizon, equity_allocation_over_time,num_sim_runs = 100)

    RPVs_array = np.zeros((num_sim_runs,planning_horizon))
    for n in range(planning_horizon):
        calculated_age = age + n
        if calculated_age < retirement_age:
            RPVs_array[i][n] = ctrbs * DF
        else:
            
    return 10


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
