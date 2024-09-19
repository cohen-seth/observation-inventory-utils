#!/bin/bash -l
# This script is for running an automation of the standard set of plots

SATINFO_DIR=/contrib/$USER/home/obs-inventory/build_gsinfo/satinfo
OZINFO_DIR=/contrib/$USER/home/obs-inventory/build_gsinfo/ozinfo
OUTPUT_LOC=/contrib/$USER/home/inventory-figures
WORK_DIR=/lustre/home/work/inventory-work

cd $(dirname $0)

source ../../obs_inv_utils_pw_inv_cluster.sh

#run plots individually to prevent connection / memory problems 
python3 ../plotting/plot_mysql_dir_sensor_sat.py --sidb $SATINFO_DIR -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor.py -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_amv.py --sidb $SATINFO_DIR -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_geo.py --sidb $SATINFO_DIR -o $OUTPUT_LOC 
python3 ../plotting/plot_mysql_sensor_sat_gps.py --sidb $SATINFO_DIR -o $OUTPUT_LOC
python3 ../plotting/plot_mysql_sensor_sat_ozone.py --sidb $OZINFO_DIR -o $OUTPUT_LOC
python3 ../plotting/plot_mysql_typ.py -o $OUTPUT_LOC 
