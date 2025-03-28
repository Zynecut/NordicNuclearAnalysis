from functions.global_functions import *



# Define global variables
YEAR_SCENARIO = 2025
case = 'Baseline'
version = 'v1'

YEAR_START = 1991
YEAR_END = 1993

DATE_START = pd.Timestamp(f'{YEAR_START}-01-01 00:00:00', tz='UTC')
DATE_END = pd.Timestamp(f'{YEAR_END}-12-31 23:00:00', tz='UTC')

loss_method = 0
new_scenario = False
save_scenario = False



# GET BASE DIRECTORY
try:
    # FOR SCRIPTS
    BASE_DIR = pathlib.Path(__file__).parent
except NameError:
    # FOR NOTEBOOKS AND INTERACTIVE SHELLS
    BASE_DIR = pathlib.Path().cwd()
    BASE_DIR = BASE_DIR / f'case_{case}'

# SQL PATH
SQL_FILE = BASE_DIR / f"powergama_{case}_{version}_{YEAR_START}_{YEAR_END}.sqlite"

# FILE PATHS
DATA_PATH = BASE_DIR / 'data'
OUTPUT_PATH = BASE_DIR / 'results'
OUTPUT_PATH_PLOTS = BASE_DIR / 'results' / 'plots'

# MAINTENANCE START ORDER FOR NUCLEAR POWER
week_MSO = {'FI_10':16,
            'FI_12':36,
            'SE3_3':20,
            'SE3_6':24,
            'GB':32,
            'NL':28
            }


# %%  === Configure Grid and Run Simulation ===
data, time_max_min = setup_grid(YEAR_SCENARIO, version, DATE_START, DATE_END, DATA_PATH, new_scenario, save_scenario, case)
res = solve_lp(data, SQL_FILE, loss_method, replace=True, nuclear_availability=0.7, week_MSO=week_MSO)
