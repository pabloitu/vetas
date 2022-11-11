import json
import logging
import os
import pandas
import numpy
from shapely.geometry import Polygon
from etas import set_up_logger
from etas.simulation import generate_catalog
from etas.inversion import round_half_up

set_up_logger(level=logging.INFO)

# todo
'''
Doc pending
'''

if __name__ == '__main__':
    numpy.random.seed(777)
    with open("artifacts/simulate_catalog_config.json", 'r') as f:
        simulation_config = json.load(f)

    region = Polygon(numpy.load(simulation_config["shape_coords"]))
    synthetic = generate_catalog(
        polygon=region,
        timewindow_start=pandas.to_datetime(simulation_config["burn_start"]),
        timewindow_end=pandas.to_datetime(simulation_config["end"]),
        parameters=simulation_config["parameters"],
        mc=simulation_config["mc"],
        beta_main=simulation_config["beta"],
        delta_m=simulation_config["delta_m"]
    )

    synthetic.magnitude = round_half_up(synthetic.magnitude, 1)
    synthetic.index.name = 'id'
    print("store catalog..")
    primary_start = simulation_config['primary_start']
    fn_store = simulation_config['fn_store']
    os.makedirs(os.path.dirname(fn_store), exist_ok=True)
    synthetic[["latitude", "longitude", "time", "magnitude"]].query(
        "time>=@primary_start").to_csv(fn_store)
    print("\nDONE!")
