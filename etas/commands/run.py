import argparse
import os
import logging
import json
import pandas
import numpy
from shapely.geometry import Polygon
from etas.commands.sim import sim, sim_time_inv
from etas import set_up_logger
from etas.commands.inv import invert_etas
from etas.inversion import ETASParameterCalculation

set_up_logger(level=logging.DEBUG)


def run(config, output_fn='simulation.csv', time_invariant=False,
        forecast_duration=30, n_sims=100, **kwargs):
    if time_invariant:
        invert_etas(config, **kwargs)
        # todo get parameter name
        sim_time_inv('output/parameters_ch.json')

    else:
        invert_etas(config, **kwargs)
        sim('output/parameters_ch.json')
    # simulation.prepare()
    # simulation.simulate_to_csv(output_fn, forecast_duration, n_sims, **kwargs)


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('config', help='Configuration file or parameter file'
                                       ' of the simulation', type=str)
    parser.add_argument('-o', '--output_fn', help='Output filename', type=str)
    parser.add_argument('-ti', '--time_invariant',
                        help='Time invariant or dependent forecast.'
                             'i.e. Follows previous sequences', type=bool)

    args = parser.parse_args()
    run(**vars(args))


if __name__ == '__main__':
    main()
