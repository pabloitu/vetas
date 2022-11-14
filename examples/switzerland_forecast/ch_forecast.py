import json
import logging

import pandas as pd
from etas import set_up_logger
from etas.inversion import ETASParameterCalculation
from etas.simulation import ETASSimulation

set_up_logger(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    # reads configuration for example forecast
    config_fn = 'ch_forecast_config.json'
    fn_store_simulation = 'output/simulations.csv'
    forecast_duration = 30
    n_simulations = 100

    with open(config_fn, 'r') as f:
        forecast_config = json.load(f)

    etas_invert = ETASParameterCalculation(forecast_config)
    etas_invert.prepare()
    etas_invert.invert()
    etas_invert.store_results(forecast_config['data_path'], True)

    simulation = ETASSimulation(etas_invert)
    simulation.prepare()

    store = pd.DataFrame()
    for chunk in simulation.simulate(forecast_duration, n_simulations):
        store = pd.concat([store, chunk],
                          ignore_index=False)

    # to store the forecast in a csv instead of just producting it,
    # do the following:
    # simulation.simulate_to_csv(fn_store_simulation, forecast_duration,
    #                            n_simulations)
    logger.debug(store)


if __name__ == '__main__':
    main()
