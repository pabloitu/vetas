import json
import logging
import os
import pandas
import numpy
from shapely.geometry import Polygon
from etas import set_up_logger
from etas.simulation import simulate_catalog
from etas.inversion import round_half_up
from etas.inversion import ETASParameterCalculation
from etas.simulation import ETASSimulation

set_up_logger(level=logging.DEBUG)

# todo
# I am in the middle of allowing the simulation __init__ to take a dict
# best not to touch the ETASSimulation class and also not this file :D
'''
Doc pending
'''


def main():
    simulation_duration = 365 # in days
    fn_parameters = os.path.join(
        os.path.dirname(__file__),
        'simulation_parameters.json')
    fn_store_simulation = os.path.join(
        os.path.dirname(__file__),
        'output/simulated_catalog.csv')
    n_sims = 1

    # Initialize simulation
    simulation = ETASSimulation(fn_parameters)
    simulation.prepare()

    # Simulate and store one catalog
    simulation.simulate_to_csv(fn_store_simulation, simulation_duration,
                               n_sims)


    # region_fn = os.path.join(os.path.dirname(__file__),
    #                          simulation_config["shape_coords"])
    # region = Polygon(numpy.load(region_fn))

    # synthetic = simulate_catalog(
    #     auxiliary_catalog=None,
    #     polygon=region,
    #     auxiliary_start=pandas.to_datetime(simulation_config["burn_start"]),
    #     primary_start=pandas.to_datetime(simulation_config["primary_start"]),
    #     simulation_end=pandas.to_datetime(simulation_config["end"]),
    #     parameters=simulation_config["theta"],
    #     mc=simulation_config["mc"],
    #     beta_main=simulation_config["beta"],
    #     delta_m=simulation_config["delta_m"]
    # )
    #
    # synthetic.magnitude = round_half_up(synthetic.magnitude, 1)
    # synthetic.index.name = 'id'
    # print("store catalog..")
    # primary_start = simulation_config['primary_start']
    # fn_store = os.path.join(os.path.dirname(__file__),
    #                         simulation_config['fn_store'])
    # os.makedirs(os.path.dirname(fn_store), exist_ok=True)
    # synthetic[["latitude", "longitude", "time", "magnitude"]].query(
    #     "time>=@primary_start").to_csv(fn_store)
    # print("\nDONE!")


if __name__ == '__main__':
    main()
