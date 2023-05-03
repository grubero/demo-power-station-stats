'''
Module to handle API requests and writing data to screen and file

1/5/2023
'''
import json
import requests

def write_to_file(text, filename):
    ''' multiple station calls made so append to file '''
    with open(filename, 'a') as fw:
        print(text, file=fw)


def json_print(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    #print(text)
    return text


def send_request(api, parameters=""):
    ''' Make api request to opennem '''
    try:
        print(f'sending api request: {api}')
        if parameters != "":
            response = requests.get(api, parameters)
        else:
            response = requests.get(api)
    except requests.exceptions.JSONDecodeError:
        print('Invalid JSON data returned')
    else:
        return response