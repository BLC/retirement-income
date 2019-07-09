import numpy as np
from decimal import Decimal, ROUND_HALF_UP

def calc_model_port_ret_across_sim_runs_at_projection_year(model_port_id,projection_year,config,num_sim_runs=100):

    mp_asset_class_column_ordering = config['asset_class_order']
    dfModelPorts = config['modelportfolios']
    DFs_asset_class_sim_run = config['simulation_returns']

    asset_class_sim_run_matrix = np.zeros((len(mp_asset_class_column_ordering), num_sim_runs))

    #Determine asset class sim run 21 x 100 matrix
    for i, name in enumerate(mp_asset_class_column_ordering):
        asset_class_sim_run_matrix[i][:] = DFs_asset_class_sim_run[name].iloc[:,projection_year]

    #Determine model_portfolio asset allocation weights 1 x 21 matrix
    model_port_asset_class_matrix = dfModelPorts.iloc[[model_port_id]]

    #Calculate model portfolio simulated output across all sim runs for specified projection year
    model_port_sim_run_output = np.matmul(model_port_asset_class_matrix, asset_class_sim_run_matrix)
    
    return model_port_sim_run_output

def lookup_closest_model_port(equity_allocation_over_time, projection_year):
    temp = round(equity_allocation_over_time[projection_year] * 100 / 0.01) * 0.01
    model_port = Decimal(temp).to_integral_value(rounding = ROUND_HALF_UP)
    return model_port