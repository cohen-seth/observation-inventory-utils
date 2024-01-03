import automation_utils as au
import atm_dicts
import yaml_generation as yg
import obs_inv_utils.obs_inv_cli as cli

import argparse

import subprocess

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-cat", dest="category", help="Category of variables to inventory. Valid options: atmosphere", choices=['atmosphere'], default="atmosphere", type=str)
parser.add_argument("-p", dest="platform", help="Platform the script is being run on. Valid options: pw, hera", choices=['pw', 'hera'], default="pw", type=str)
args = parser.parse_args()

#get category list
# more categories to be added as they are written as dictionaries 
# remember to add new categories to the argparser options and here
to_inventory = []
if args.category is 'atmosphere':
    to_inventory = atm_dicts.atm_infos 

#need to run correct sh for platform 
if args.platform is 'pw':
    subprocess.run(['source', '../../obs_inv_utils_pw_cloud.sh'])
elif args.platform is 'hera':
    subprocess.run(['source', '../../obs_inv_utils_hera.sh'])


#define functions to run in parallel 
def run_obs_inventory(inventory_info):
    #EXPAND THIS LATER TO HANDLE TWO DAY RUNS; probably specify end time as part fo the argument options above
    end_time = inventory_info.end_time
    yaml_file = yg.generate_obs_inv_config(inventory_info, end_time)
    cli.get_obs_inventory(yaml_file)

def run_nceplibs(inventory_info):
    #ADD TWO DAY EXPANSION HERE AS WELL
    end_time = inventory_info.end_time 
    yaml_file = yg.generate_nceplibs_inventory_config(inventory_info, end_time)
    
    #run correct command
    if inventory_info.nceplibs_cmd == au.NCEPLIBS_SINV:
        cli.get_obs_count_meta_sinv(yaml_file)
    elif inventory_info.nceplibs_cmd == au.NCEPLIBS_CMPBQM:
        cli.get_obs_count_meta_cmpbqm(yaml_file)
    else:
        print(f'No valid commmand found for nceplibs_cmd in {inventory_info.obs_name} inventory info with value: ' + inventory_info.nceplibs_cmd)


#for each 
# generate yaml for obs inventory
# run obs inventory
# determine nceplibs command (sinv or cmpbqm)
# generate yaml for nceplibs
# run correct command 

