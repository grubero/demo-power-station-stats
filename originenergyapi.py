#!/usr/bin/env python
'''
Gather power generation statistics of Origin Energy power stations across Australia.

No public AEMO API is available. Using opennem.org.au project instead.

Run 'python originenergyapi.py -h' for usage commands

Author: Oliver Gruber
3/5/2023
'''

import argparse
import textwrap
from pathlib import Path

from tabulate import tabulate
from requesthandling import send_request
from requesthandling import json_print
from requesthandling import write_to_file

def factory(aClass, *pargs, **kargs):
    return aClass(*pargs, **kargs)


class PowerStation():
    def __init__(self, power_station_code, type, power, emissions, market_value):
        self.power_station_code = power_station_code
        self.type = type
        self.power = power
        self.emissions = emissions
        self.market_value = market_value

    def get_power_station_code(self):
        return self.power_station_code

    def get_type(self):
        return self.type
    
    def get_power(self):
        return self.power
    
    def get_emissions(self):
        return self.emissions
    
    def get_market_value(self):
        return self.market_value
    

def clear_outputfile(filename):
    output_filename = filename
    p = Path(output_filename)

    if p.is_file():
        with open(p, 'w') as fw:
            print('', file=fw) # safer method to overwrite with an empty .txt file than using riskier os.remove()


power_stations = [] # object list

def get_power_station_stats(power_generation_sites):
    for station_code in range(len(power_generation_sites)):
        response = send_request('https://api.opennem.org.au/stats/energy/station/nem/' + \
                                power_generation_sites[station_code]['apicode'])
        write_to_file(json_print(response.json()), 'stationstats.txt')

        power_station_power = []
        power_station_emissions = []
        power_station_market_value = []
        power_station_code = power_generation_sites[station_code]['apicode']
        power_station_type = power_generation_sites[station_code]['type']
        
        for generator in range(len(response.json()['data'])):
            response.json()['data'][generator]['history']['data']

            ''' gather power output per generator per power station '''
            if response.json()['data'][generator]['data_type'] == 'energy':
                 power_station_power.append({'gen_code': response.json()['data'][generator]['code'], \
                    'history': response.json()['data'][generator]['history']['data']})                

            ''' gather emissions per generator per power station '''
            if response.json()['data'][generator]['data_type'] == 'emissions':
                 power_station_emissions.append({'gen_code': response.json()['data'][generator]['code'], \
                    'history': response.json()['data'][generator]['history']['data']})
                          
            ''' gather market value per generator per power station '''
            if response.json()['data'][generator]['data_type'] == 'market_value':
                 power_station_market_value.append({'gen_code': response.json()['data'][generator]['code'], \
                    'history': response.json()['data'][generator]['history']['data']})                 

        power_stations.append(factory(PowerStation, power_station_code, power_station_type, power_station_power, \
            power_station_emissions, power_station_market_value))


def use_custom_api(api, filename, parameters=''):
    '''' make a user specified api request from CLI '''
    response = send_request(api, parameters)

    write_to_file(json_print(response.json()), filename)
    json_print(response.json())


def show_origin_energy_power_generation_sites():
    '''' store site codes in a function instead of global variable (easier for unittesting) '''

    origin_energy_power_generation_sites = (
    {'apicode': 'CHALLWF', 'type': 'wind farm', 'name': 'Challicum Hills Wind Farm', 'location': 'Ararat, VIC'},
    {'apicode': 'CULLERIN', 'type': 'wind farm', 'name': 'Cullerin Range Wind Farm', 'location': 'Upper Lachlan Shire, NSW'},
    {'apicode': 'DAYDSF', 'type': 'solar farm', 'name': 'Daydream Solar Farm', 'location': 'Collinsville, QLD'},  
    {'apicode': 'DDPS1', 'type': 'gas', 'name': 'Darling Downs Power Station', 'location': 'Kogan, QLD'},
    {'apicode': 'DDSF', 'type': 'solar farm', 'name': 'Darling Downs Solar Farm', 'location': 'Kogan, QLD'},
    {'apicode': 'ERARING', 'type': 'coal', 'name': 'Eraring Power Station', 'location': 'Dora Creek, NSW'},
    {'apicode': 'ERGT01', 'type': 'coal', 'name': 'Eraring Power Station', 'location': 'Dora Creek, NSW'},
    {'apicode': 'LADBROKE', 'type': 'gas', 'name': 'Ladbroke Grove Power Station', 'location': 'Monbulla, SA'},
    {'apicode': 'MORTLK', 'type': 'gas', 'name': 'Mortlake Grove Power Station', 'location': 'Mortlake, VIC'},
    {'apicode': 'QUARANTN', 'type': 'gas', 'name': 'Quarantine Power Station', 'location': 'Adelaide, SA'},
    {'apicode': 'URANQ', 'type': 'gas', 'name': 'Uranquinty Power Station', 'location': 'Uranquinty, NSW'})

    return origin_energy_power_generation_sites


def history_appender(power_station, generator):
    row = [power_station.get_power_station_code(), generator['gen_code'], power_station.get_type()]
    for day in range(7):
        value = generator['history'][day]
        row.append('%d' % value)
    
    table.append(row)
    return table


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Show power generation statistics of Origin Energy power stations across Australia',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            originenergyapi.py -l # list Origin Energy power generation sites
            originenergyapi.py -c '/stats/power/network/fueltech/nem/nsw1' nsw_stats.txt # get power demand
                statistics of NSW and output to 'nsw_stats.txt'
            
            api docs: https://api.opennem.org.au/docs#operation/networks_networks_get'
    '''))

    parser.add_argument('-l', '--list', action='store_true', help='list power station codes')
    parser.add_argument('-g', '--genenergy', action='store_true', help='show energy generation')
    parser.add_argument('-e', '--emissions', action='store_true', help='show emissions per station')
    parser.add_argument('-m', '--marketvalue', action='store_true', help='show market value per station')
    parser.add_argument('-c', '--customapi', type=str, nargs=2, metavar=('apisuffix', 'outputfilename'), \
                        help='append a custom api and output results to file')
    args = parser.parse_args()

    origin_energy_power_generation_sites = show_origin_energy_power_generation_sites()

    if args.list:
        table = []
        for station in range(len(origin_energy_power_generation_sites)):
            table.append(origin_energy_power_generation_sites[station])
            
        print(tabulate(table))

    if not args.list:
        ''' any other option apart from listing sites will generate an output file '''
        clear_outputfile('stationstats.txt')

    headers=['Station Code', 'Gen Code', 'Gen Type', 'Day1', 'Day2', 'Day3', 'Day4', 'Day5', 'Day6', 'Day7']

    if args.genenergy:
        ''' display generator power statistics over previous week '''

        get_power_station_stats(origin_energy_power_generation_sites)
        table = []
        for power_station in power_stations:
            for generator in power_station.get_power():
                table = history_appender(power_station, generator)

        print('\nPower (MWh) per generator at each Origin Energy power station')
        print(tabulate(table, headers))

    if args.emissions:
        ''' display generator emissions statistics over previous week '''

        get_power_station_stats(origin_energy_power_generation_sites)
        table = []
        for power_station in power_stations:
            for generator in power_station.get_emissions():
                table = history_appender(power_station, generator)

        print('\nEmissions (tCO2e) per generator at each Origin Energy power station')
        print(tabulate(table, headers))

    if args.marketvalue:
        ''' display generator market value statistics over previous week '''

        get_power_station_stats(origin_energy_power_generation_sites)       
        table = []
        for power_station in power_stations:
            for generator in power_station.get_market_value():
                table = history_appender(power_station, generator)

        print('\nMarket value (AUD) per generator at each Origin Energy power station')
        print(tabulate(table, headers))

    
    parameters = {
        'interval': '1d', 'period': '7d' # api month parameter for power network region by fueltech is broken
    }

    if args.customapi:
        ''' send a custom api. Read https://api.opennem.org.au/docs for api format '''

        ''' getting optional parameters through argparse needs to be fixed '''

        api = "https://api.opennem.org.au" + str(args.customapi[0].strip('\'')) 
        print(f'{api} to output file {args.customapi[1]}')
        use_custom_api(api, args.customapi[1])

