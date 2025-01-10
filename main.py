#!/usr/bin/env python3

import pandas as pd
import sys
import json
import math


def convert(filename: str):
    out = "".join(filename.split('.')[:-1])
    
    header_row_index = 6 

    def get_range(cols: list[str]):
        ind = -1
        cols = cols[1:]
        for i in range(len(cols)):
            ind = i
            if 'Unnamed' not in cols[i]: 
                break
        return ind + 1
            

    df = pd.read_excel(filename,header=header_row_index)
    ind = get_range(list(df.columns))
    df.iloc[:, :ind] = df.iloc[:, :ind].fillna(method='ffill')
    df = df[df.map(lambda x: isinstance(x, (int, float)) and pd.notna(x)).any(axis=1)]
    cols = df.columns[:ind]
    df.set_index(list(cols), inplace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    dic = df.to_dict(orient='index')

    def nest_list(data):
        if len(data) == 1:
            return data[0] 
        return {data[0]: nest_list(data[1:])}
    def nest(d: dict):
        final = []
        for _key, val in d.items():
            key = list(_key)
            key = [item for item in key if not (isinstance(item, float) and math.isnan(item))]
            keyval = key + [val]
            nested = nest_list(keyval)
            final.append(nested)
        return final

    res = nest(dic)
    with open(f'{out}.json', 'w') as fp:
        js = json.dumps(res)
        fp.write(js)

if __name__ == '__main__':
    _args = sys.argv
    if len(_args) < 2:
        print('Usage: Give filepath')
        exit(1)

    args = _args[1:]
    for arg in args:
        convert(arg)