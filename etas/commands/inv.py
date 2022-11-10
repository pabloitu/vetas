import argparse
import numpy
import json
import logging
from etas import set_up_logger

from etas.inversion import ETASParameterCalculation

set_up_logger(level=logging.DEBUG)


def invert_etas(fileinput):
    with open(fileinput, 'r') as f:
        inversion_config = json.load(f)
    calculation = ETASParameterCalculation(inversion_config)
    calculation.prepare()
    calculation.invert()
    calculation.store_results(inversion_config['data_path'])


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('config', help='Configuration file of the inversion')
    # todo: add verbose and other extra options
    # todo: do we want to modify config parameters here from the cmd?
    args = parser.parse_args()
    invert_etas(**vars(args))


if __name__ == '__main__':
    main()
