#!/usr/bin/env python
# coding: utf-8

import matplotlib.pyplot as plt
import numpy as np
import pandas , matplotlib.pyplot as plt
from datetime import datetime, date
import matplotlib.dates as mdates
import os
import argparse
import obs_inv_utils.inventory_table_factory as itf
import plot_utils as utils

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-o", dest='out_dir', help="output directory for figures",default='figures',type=str)
parser.add_argument("-dev", dest='dev', help='Use this flag to add a timestamp to the filename for development', default=False, type=bool)
args = parser.parse_args()

#parameters
daterange=[date(1975,1,1), date(2025,1,1)]

def plot_one_line(dftmp, yloc):
    plt.plot(dftmp.datetime, yloc*dftmp.tot.astype('bool'),'|',color='black',markersize=5)

def select_typ(typ, db_frame):
    dftmp = db_frame.loc[db_frame['typ']==typ]
    return dftmp

def get_sensor(row):
    directory = row['parent_dir']
    sensor = directory.split("/")[2]
    return sensor


#read data from sql database of obs counts
db_frame = utils.get_distinct_prepbufr()

db_frame['datetime'] = pandas.to_datetime(db_frame.obs_day)
db_frame['sensor'] = db_frame.apply(get_sensor, axis=1)

#loop and plot typ
unique_typ = db_frame.drop_duplicates('typ').sort_values('typ', ascending=False)
step=0.05
height=step*len(unique_typ)

#make list of typ labels
typ_labels = []
for index, row in unique_typ.iterrows():
    if row.typ in utils.typ_dictionary.keys():
        typ_labels.append(utils.typ_dictionary[row.typ])
    else:
        typ_labels.append(row.typ)

fig = plt.figure(dpi=300)
fig.patch.set_facecolor('white')
ax = fig.add_axes([0, 0.1, 1, height+step])
plt.title("Inventory of NNJA Conventional Sensors")
plt.xlabel('Observation Date')
plt.ylabel('typ')

counter=0
# for index, row in unique_sat_id.iterrows():
for index, row in unique_typ.iterrows():
    pandas.options.mode.chained_assignment = None
    dftmp = select_typ(row['typ'], db_frame)
    pandas.options.mode.chained_assignment = 'warn'

    plot_one_line(dftmp, step/2+step*counter)
    counter = counter + 1

ax.set_yticks(step/2+step*np.arange(counter))
ax.set_yticklabels(typ_labels)
ax.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax.set_xlim(daterange)
ax.set_ylim([0, height])
ax.grid(which='major',color='grey', linestyle='-', linewidth=0.5)
ax.grid(which='minor', color='grey', linestyle='--', linewidth=0.2)
ax_dup = ax.twiny()
ax_dup.xaxis.set_major_locator(mdates.YearLocator(5,month=1,day=1))
ax_dup.xaxis.set_minor_locator(mdates.YearLocator(1,month=1,day=1))
ax_dup.set_xlim(daterange)

plt.suptitle(f'accurate as of {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} UTC', y=-0.01)
file_name = "all_line_observations_inventory_typ.png"
if args.dev:
    file_name = "all_line_observations_inventory_typ_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".png"
fnout=os.path.join(args.out_dir,file_name)
print(f"saving {fnout}")
plt.savefig(fnout, bbox_inches='tight')

