'''
File for collecting constants and utility functions used for the automated inventory system
'''
from collections import namedtuple

#constants
NCEPLIBS_SINV = 'sinv'
NCEPLIBS_CMPBQM = 'cmpbqm'

CLEAN_PLATFORM = 'aws_s3_clean'
REANALYSIS_BUCKET = 'noaa-reanlyses-pds'

InventoryInfo = namedtuple(
    'InventoryInfo',
    [
        'obs_name',
        'key',
        'start',
        'platform',
        'cycling_interval',
        's3_bucket',
        's3_prefix',
        'bufr_files',
        'nceplibs_cmd'
    ]
)
