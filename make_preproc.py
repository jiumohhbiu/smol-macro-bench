#!/usr/bin/python3


import argparse
import json
import statistics
import numpy as np
import os


ELEMENTS_SEP=' '


class Preprocesser:
    def __init__(self, funcs):
        self.function_set = dict()
        for func in funcs:
            self.function_set[func.__name__] = func


def mean(arr):
    return statistics.mean(arr)

def median(arr):
    return statistics.median(arr)

def percentile_5(arr):
    return np.percentile(arr, 5)

def percentile_25(arr):
    return np.percentile(arr, 25)

def percentile_75(arr):
    return np.percentile(arr, 75)

def percentile_95(arr):
    return np.percentile(arr, 95)

def main():
    parser = argparse.ArgumentParser(
        prog='Preprocess gathered data')
    parser.add_argument('-i', '--input-file', nargs='?', default='config.json')
    parser.add_argument('-a', '--apps', nargs='?', default='apps_info.txt')

    args = parser.parse_args()
    preprocesser = Preprocesser([min, max, mean, median, percentile_5, percentile_25, percentile_75, percentile_95])

    with open(args.input_file, "r") as f:
        configuration = json.load(f)
    preprocessings = configuration['var']['processing']

    with open(args.apps, "r") as input_file:
        lines = input_file.readlines()
    for variant, config in preprocessings.items():
        datasets = {}

        realizations = config['realizations'].split(ELEMENTS_SEP)
        x_axis = config['x_axis']
        if 'y_axis' in config:
            y_axis = config['y_axis']
        else:
            y_axis = None
        markers = config['markers'].split(ELEMENTS_SEP)
        filters = config['filter_options_value']
        for line in lines:
            point = line.split(',')[0]
            point_realization = point.split(ELEMENTS_SEP)[0]
            if not point_realization in realizations:
                continue

            point_x_value = None
            point_y_value = None
            dataset_key = [point_realization]
            for param in point.split(ELEMENTS_SEP)[1:]:
                k, v = param.split('=')
                
                # if filters[k]

                if k == x_axis:
                    point_x_value = float(v)
                elif y_axis and k == y_axis:
                    point_y_value = float(v)
                else:
                    dataset_key.append(param)
            dataset_key = ELEMENTS_SEP.join(dataset_key)
            point = 'data/' + point + '.txt'
            with open(point, "r") as p:
                timings = list(map(int, p.readlines()))

                values = [point_x_value]
                if point_y_value != None:
                    values.append(point_y_value)

                for marker in markers:
                    values.append(preprocesser.function_set[marker](timings))

                if not dataset_key in datasets:
                    datasets[dataset_key] = []
                datasets[dataset_key].append(values)

        for params, data in datasets.items():
            variant_path = 'preproc_data/' + variant + '/' + params + ('.txt' if y_axis is None else '.dat')
            os.makedirs(os.path.dirname(variant_path), exist_ok=True)
            with open(variant_path, "w") as f:
                data_sorted = sorted(data)
                last_x = None
                for line in data_sorted:
                    if y_axis != None and last_x != line[0]:
                        f.write("\n")
                    last_x = line[0]
                    formatted_line = "\t".join(map(str, line))
                    f.write(f'{formatted_line}\n')


if __name__ == '__main__':
    main()
