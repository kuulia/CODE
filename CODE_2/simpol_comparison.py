#Author: Linus Lind Jan. 2024
#GNU General Public License v3.0
#calculates MAE, MSE and STD of data set 
import pandas as pd
import numpy as np
import math
from os import path
    
def atm_to_log_kpa(df: pd.DataFrame) -> pd.DataFrame:
    return df.apply(lambda atm : math.log10(atm * 101.325))

def calc_abs_error(pred: pd.DataFrame, target: pd.DataFrame) -> pd.DataFrame:
    diff = target - pred
    return diff.apply(lambda e: abs(e))

def calc_mae(abs_errors: pd.DataFrame) -> pd.DataFrame:
    return np.mean(abs_errors)

def calc_mse(abs_errors: pd.DataFrame) -> pd.DataFrame:
    return np.mean(np.square(abs_errors))

def main():
    filepath = path.relpath("data")
    #load simpol groups
    simpol_predictions_raw = pd.read_csv(\
        path.join(filepath, 'lumiaro_processed_finalSG_props_288_uncorrected.csv'))
    
    simpol_psat_atm = simpol_predictions_raw['p0']

    pred_log_p_sat = pd.DataFrame()
    pred_log_p_sat['p0'] = atm_to_log_kpa(simpol_psat_atm)

    pred_log_p_sat.to_csv('data/simpol_uncorrected_log_p_sat.txt', index=None, header=False)
    #print(f'\nThe predicted saturation vapour pressures are:\n {pred_log_p_sat}')

    wang_data = pd.read_csv('data/wang_data.csv')
    wang_data['simpol'] = pred_log_p_sat['p0'] 
    wang_data = wang_data[wang_data['volatility'] == 'VOC']
    print(wang_data)
    target_log_p_sat = pd.DataFrame()
    target_log_p_sat['p0'] = wang_data['log_p_sat']
    #print(f'\nThe target saturation vapour pressures are:\n {target_log_p_sat}')

    abs_errors = calc_abs_error(wang_data['simpol'], wang_data['log_p_sat'])
    print(f'\nThe absolute errors are:\n{abs_errors}')
    print(f'\nThe MAE is: {calc_mae(abs_errors)}')
    print(f'\nThe MSE is: {calc_mse(abs_errors)}')
    print(f'\nThe STD of errors is: {np.std(abs_errors, axis=0)}')
    print('\n')

if __name__ == "__main__":
    main()