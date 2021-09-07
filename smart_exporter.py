#!/usr/bin/env python3

import glob
import re
import subprocess
import json
import pprint

# S.M.A.R.T. exporter for Prometheus

OUTPUT_ID_LIST = [
    1,      # Raw_Read_Error_Rate
    5,      # Reallocated_Sector_Ct
    194,    # Temperature_Celsius
    196,    # Reallocated_Event_Count
    197,    # Current_Pending_Sector
    198,    # Offline_Uncorrectable
]

def run(cmd):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    stdout, stderr = proc.communicate()

    if proc.returncode != 0:
        if stderr:
            raise Exception(stderr.decode('utf-8'))

    return json.loads(stdout)

def smart_status(dev):
    result = run(['smartctl', '-j', '-x', dev])

    if ('ata_smart_attributes' not in result):
        return {}

    status = { 'serial': result['serial_number'] }
    for param in result['ata_smart_attributes']['table']:
        if (param['id'] in OUTPUT_ID_LIST):
            if (param['id'] == 194):
                status[param['name']] = int(re.search(r'\d+', param['raw']['string']).group())
            else:
                status[param['name']] = param['raw']['value']

    return status


drive_list = list(filter(lambda dev: re.match('^/dev/(sd[a-z]+)$', dev),
                         glob.glob('/dev/*')))

for dev in drive_list:
    status = smart_status(dev)

    for param,value in status.items():
        if (param == 'serial'):
            continue
        print('HDD_{param}{{serial="{serial}",dev="{dev}"}} {value}'.format(
            dev=dev,
            param=param,
            serial=status['serial'],
            value=value
        ))
