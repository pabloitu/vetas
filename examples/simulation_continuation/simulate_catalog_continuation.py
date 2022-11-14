#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
# simulation of catalog continuation (for forecasting)
#
# as described by Mizrahi et al., 2021
# Leila Mizrahi, Shyam Nandan, Stefan Wiemer;
# Embracing Data Incompleteness for Better Earthquake Forecasting.
# Journal of Geophysical Research: Solid Earth.
# doi: https://doi.org/10.1029/2021JB022379
###############################################################################


import json
import logging

from etas import set_up_logger
from etas.inversion import ETASParameterCalculation
from etas.simulation import ETASSimulation

set_up_logger(level=logging.INFO)


def main():
    # Simulation parameters.
    forecast_duration = 365
    fn_inversion_output = "inversion_input/parameters_0.json"
    fn_store_simulation = "output/simulated_catalog_continuation.csv"
    n_sims = 1

    # Load ETAS parameters
    etas_inversion_reload = ETASParameterCalculation.load_calculation(
        fn_inversion_output)

    # Initialize simulation
    simulation = ETASSimulation(etas_inversion_reload)
    simulation.prepare()

    # Simulate and store one catalog
    simulation.simulate_to_csv(fn_store_simulation, forecast_duration, n_sims)


if __name__ == '__main__':
    main()
