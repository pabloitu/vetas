import argparse
import os
import logging
import json
import pandas
import numpy
from shapely.geometry import Polygon
from etas import set_up_logger
from etas.simulation import generate_catalog
from etas.inversion import round_half_up

set_up_logger(level=logging.DEBUG)


def simulate_catalog(config, seed=None):
    with open(config, 'r') as f:
        config = json.load(f)
    if seed:
        numpy.random.seed(seed)
    region = Polygon(numpy.load(config["shape_coords"]))

    synthetic = generate_catalog(
        polygon=region,
        timewindow_start=pandas.to_datetime(config["burn_start"]),
        timewindow_end=pandas.to_datetime(config["end"]),
        parameters=config["parameters"],
        mc=config["mc"],
        beta_main=config["beta"],
        delta_m=config["delta_m"]
    )

    synthetic.magnitude = round_half_up(synthetic.magnitude, 1)
    synthetic.index.name = 'id'
    print("store catalog..")
    primary_start = config['primary_start']
    fn_store = config['fn_store']
    os.makedirs(os.path.dirname(fn_store), exist_ok=True)
    synthetic[["latitude", "longitude", "time", "magnitude"]].query(
        "time>=@primary_start").to_csv(fn_store)
    print("\nDONE!")


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('config', help='Configuration file of the inversion')
    # todo: add verbose and other extra options
    # todo: do we want to modify config parameters here from the cmd?
    args = parser.parse_args()
    simulate_catalog(**vars(args))


if __name__ == '__main__':
    main()
