#!/usr/bin/python3


import argparse
import json
import pprint
from itertools import product


ELEMENTS_SEP=' '


def apply_repr(key, value, repr):
    return repr.format(KEY=key, VALUE=value)


def main():
    parser = argparse.ArgumentParser(
        prog='Retrive apps')
    parser.add_argument('-i', '--input-file', nargs='?', default='config.json')

    args = parser.parse_args()

    with open(args.input_file, "r") as f:
        configuration = json.load(f)

    lines = []
    default_repr = configuration['var']['default_repr']
    for r in configuration['realizations']:
        options_path = []
        options_builder = []
        for option in configuration['realizations'][r]['options']:
            key = option
            values = configuration['realizations'][r]['options'][option]['values'].split(ELEMENTS_SEP)
            repr = configuration['realizations'][r]['options'][option]['repr']
            options_builder.append([apply_repr(key, value, repr) for value in values])
            options_path.append([apply_repr(key, value, default_repr) for value in values])

        apps_names = []
        for option_path in product(*options_path):
            apps_names.append(' '.join(map(str, option_path)))

        builder_options_combinations = []
        for builder_options in product(*options_builder):
            builder_options_combinations.append(' '.join(map(str, builder_options)))

        files = configuration['realizations'][r]['files']
        target = configuration['realizations'][r]['target']
        build_exec = configuration['realizations'][r]['build_exec']

        for path, builder_options in zip(apps_names, builder_options_combinations):
            print(f'{r} {path},{builder_options},{files},{target},{build_exec}')


if __name__ == '__main__':
    main()
