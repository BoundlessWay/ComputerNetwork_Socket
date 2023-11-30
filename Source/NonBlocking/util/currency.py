#!/usr/bin/env python3
# currency.py
"""
This module provides some exchange rate API
"""

import json
from urllib.request import urlopen
import datetime
import os

cwd = os.path.abspath(os.getcwd())
db_path = os.path.join(cwd, 'database/') 

if not os.path.exists(db_path):
    os.makedirs(db_path)

db_path = db_path + 'data.json'

baseURL = 'http://api.exchangeratesapi.io/v1/'
key = 'access_key=19oj1mzWrYinMYZ7qGywoY1O4gvB2dld'
today = datetime.date.today().isoformat()

def fetch_latest(): 
    request = ''.join((baseURL, 'latest?', key))
    data = json.loads(urlopen(request).read().decode())
    date = data['date']
    data = {data['date']:data['rates']}

    if not os.path.isfile(db_path):
        with open(db_path, 'w') as file:
            pass

    with open(db_path, "r") as file:
        db = file.read()
        if not db:
            db = {}
        else:
            db = json.loads(db)
 
    db.update(data)
 
    with open(db_path, "w") as file:
        json.dump(db, file)

    return data[date]

def fetch_historical(date):
    request = ''.join((baseURL, date, '?', key))
    data = json.loads(urlopen(request).read().decode())
    data = {data['date']:data['rates']}

    if not os.path.isfile(db_path):
        with open(db_path, 'w') as file:
            pass

    with open(db_path, "r") as file:
        db = file.read()
        if not db:
            db = {}
        else:
            db = json.loads(db)

    db.update(data)

    with open(db_path, "w") as file:
        json.dump(db, file)

    return data[date]

def fetch_timeseries(start_date, end_date):
    request = 'https://api.exchangerate.host/timeseries?' \
        + 'start_date=' + start_date \
        + '&end_date=' + end_date 
    print(request)
    data = json.loads(urlopen(request).read().decode())
    data = data['rates']

    if not os.path.isfile(db_path):
        with open(db_path, 'w') as file:
            pass

    with open(db_path, "r") as file:
        db = file.read()
        if not db:
            db = {}
        else:
            db = json.loads(db)
 
    db.update(data)

    with open(db_path, "w") as file:
        json.dump(db, file)

    return data

def historical(date, symbols_list=None):
    if not os.path.isfile(db_path):
        data = fetch_historical(date)
    else:
        with open(db_path, 'r') as file:
            try:
                data = json.load(file)[date]
            except KeyError:
                data = fetch_historical(date)
    
    if symbols_list:
        return {key.upper():data[key.upper()] for key in symbols_list}
    return data

def latest(symbols_list=None):
    data = fetch_latest()

    if symbols_list:
        return {key.upper():data[key.upper()] for key in symbols_list}
    return data

def convert(src, dst, amount, date=None):
    if not date:
        data = fetch_latest()
    else:
        with open(db_path, 'r') as file:
            try:
                data = json.load(file)[date]
            except KeyError:
                data = fetch_historical(date)

    src = data[src.upper()]
    dst = data[dst.upper()]
    return dst*float(amount) / src

def timeseries(start_date, end_date, symbols_list=None):
    data = fetch_timeseries(start_date, end_date)

    if symbols_list:
        for date, _ in data.items():
            try:
                data[date] = {symbol.upper():data[date][symbol.upper()] for symbol in symbols_list}
            except KeyError:
                continue
    return data