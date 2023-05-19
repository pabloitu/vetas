import argparse
import os
import logging
import json
import pandas
import numpy
from shapely.geometry import Polygon
from etas import set_up_logger
from etas.simulation import simulate_catalog, ETASSimulation
from etas.inversion import round_half_up, read_shape_coords, \
    ETASParameterCalculation

set_up_logger(level=logging.DEBUG)


def parse_config(config_fn):
    with open(config_fn, 'r') as f:
        config = json.load(f)
    return True if 'fn_catalog' in config else False


def sim_time_inv(config_fn):
    _path = os.path.abspath(os.path.dirname(config_fn))

    with open(config_fn, 'r') as f:
        config = json.load(f)

    if config["shape_coords"].endswith(('.npy', '.txt')):
        region = Polygon(
            numpy.load(os.path.join(_path, config["shape_coords"])))
    else:
        region = read_shape_coords(config["shape_coords"])

    synthetic = simulate_catalog(
        polygon=region,
        timewindow_start=pandas.to_datetime(config["burn_start"]),
        timewindow_end=pandas.to_datetime(config["end"]),
        parameters=config["theta"],
        mc=config["mc"],
        beta_main=config["beta"],
        delta_m=config["delta_m"]
    )

    synthetic.magnitude = round_half_up(synthetic.magnitude, 1)
    synthetic.index.name = 'id'
    print("store catalog..")
    primary_start = config['primary_start']
    fn_store = os.path.join(_path, config['fn_store'])
    os.makedirs(os.path.dirname(fn_store), exist_ok=True)
    synthetic[["latitude", "longitude", "time", "magnitude"]].query(
        "time>=@primary_start").to_csv(fn_store)
    print("\nDONE!")


def sim(parameter_fn, output_fn='simulation.csv',
        forecast_duration=365, n_sims=1, **kwargs):
    etas_inversion_reload = ETASParameterCalculation.load_calculation(
        parameter_fn)

    simulation = ETASSimulation(etas_inversion_reload)
    simulation.prepare()

    simulation.simulate_to_csv(output_fn, n_sims, forecast_duration, **kwargs)


def sim_catalog(config, seed=None, **kwargs):
    exist_auxcat = parse_config(config)

    if seed:
        numpy.random.seed(seed)

    if exist_auxcat:
        print('time Variant')
        sim(config, **kwargs)
    else:
        sim_time_inv(config, **kwargs)


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('parameter_fn',
                        help='Configuration file or parameter file'
                             ' of the simulation', type=str)
    parser.add_argument('-o', '--output_fn', help='Output filename', type=str)
    parser.add_argument('-t', '--forecast_duration',
                        help='Duration of the forecast (in days)', type=int)
    parser.add_argument('-n', '--n_sims',
                        help='Number of synthetic catalogs', type=int)
    parser.add_argument('-mt', '--m_threshold',
                        help='Magnitude threshold of the simulation',
                        type=float)
    parser.add_argument('-s', '--seed',
                        help='Seed for pseudo-random number generation',
                        type=int)
    parser.add_argument('-f', '--fmt',
                        help='Output format',
                        type=str)
    args = parser.parse_args()
    sim(**vars(args))


if __name__ == '__main__':
    main()
