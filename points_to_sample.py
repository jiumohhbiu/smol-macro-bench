#!/usr/bin/python3


import argparse
import random
import json


ELEMENTS_SEP=' '


def apply_repr(key, value, repr):
    return repr.format(KEY=key, VALUE=value)


def rse(timings):
    if len(timings) < 15:
        return 1

    t_avg = sum(timings) / len(timings)
    def disp(timings):
        return sum([(t_i - t_avg) ** 2 for t_i in timings]) / len(timings)

    def std_deviation(timings):
        return disp(timings) ** 0.5

    def std_err(timings):
        return std_deviation(timings) / (len(timings) ** 0.5)

    return std_err(timings) / t_avg


def main():
    parser = argparse.ArgumentParser(
        prog='Generate update sequence')
    parser.add_argument('-i', '--input-file', nargs='?', default='config.json')
    parser.add_argument('-a', '--apps', nargs='?', default='apps_info.txt')
    parser.add_argument('-o', '--output-file', nargs='?', default='points_to_sample.txt')

    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        configuration = json.load(f)

    rse_target = float(configuration['var']['halt_on'])
    with open(args.apps, "r") as input_file:
        lines = input_file.readlines()
    with open(args.output_file, "w") as output_file:
        for line in lines:
            point = line.split(',')[0]
            point = 'data/' + point + '.txt'
            try:
                with open(point, "r") as p:
                    timings = list(map(int, p.readlines()))
                    rse_current = rse(timings)
                    # print(rse_current)
                    if not rse_current < rse_target:
                        output_file.write(line)
            except FileNotFoundError:
                output_file.write(line)


if __name__ == '__main__':
    main()
