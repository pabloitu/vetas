import argparse
import numpy
import json
import logging
from etas import set_up_logger

from etas.inversion import ETASParameterCalculation

set_up_logger(level=logging.DEBUG)


def invert_etas(fileinput, mc_min=0.1):
    with open(fileinput, 'r') as f:
        inversion_config = json.load(f)
    calculation = ETASParameterCalculation(inversion_config)
    calculation.prepare()
    parameters = calculation.invert()
    print(calculation, parameters)
    # calculation.store_results(inversion_config['data_path'])


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('fileinput', help='file containing magnitudes')
    # parser.add_argument('fileoutput', help='file containing magnitudes')
    parser.add_argument('-min', '--mc_min', help='min search mc', type=float)

    args = parser.parse_args()
    invert_etas(**vars(args))


if __name__ == '__main__':
    main()
