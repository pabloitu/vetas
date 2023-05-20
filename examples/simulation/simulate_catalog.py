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

set_up_logger(level=logging.INFO)

# todo
# I am in the middle of allowing the simulation __init__ to take a dict
# best not to touch the ETASSimulation class and also not this file :D
'''
Doc pending
'''


def main():
    fn_parameters = os.path.join(
        os.path.dirname(__file__),
        'simulation_parameters.json')
    fn_store_simulation = os.path.join(
        os.path.dirname(__file__),
        'output/simulated_catalog.csv')
    n_sims = 1

    # Initialize simulation
    simulation = ETASSimulation(fn_parameters)
    # simulation.prepare()

    # Simulate and store one catalog
    simulation.simulate_to_csv(fn_store_simulation,
                               n_simulations=n_sims)


if __name__ == '__main__':
    main()
