#Author: Linus Lind Jan. 2024
#GNU General Public License v3.0
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
    filepath = path.relpath("CODE_2/data")
    #load simpol groups
    simpol_predictions_raw = pd.read_csv(\
        path.join(filepath, 'geckoQ_processed_finalSG_props_298_uncorrected_231123.csv'))
    
    simpol_psat_atm = simpol_predictions_raw['p0']

    pred_log_p_sat = pd.DataFrame()
    pred_log_p_sat['p0'] = atm_to_log_kpa(simpol_psat_atm)

    pred_log_p_sat.to_csv('CODE_2/data/simpol_uncorrected_log_p_sat.txt', index=None, header=False)
    print(f'\nThe predicted saturation vapour pressures are:\n {pred_log_p_sat}')

    target_log_p_sat = pd.read_csv(\
        path.join(filepath + '/geckoq_all', 'geckoq_log_p_sat.txt'), header=None)
    target_log_p_sat.columns = ['p0']
    print(f'\nThe target saturation vapour pressures are:\n {target_log_p_sat}')

    abs_errors = calc_abs_error(pred_log_p_sat, target_log_p_sat)
    print(f'\nThe absolute errors are:\n{abs_errors}')
    print(f'\nThe MAE is: {calc_mae(abs_errors)}')
    print(f'\nThe MSE is: {calc_mse(abs_errors)}')
    print(f'\nThe STD of errors is: {np.std(abs_errors, axis=0).iloc[0]}')
    print('\n')

if __name__ == "__main__":
    main()