import json
import logging
from etas import set_up_logger
from pprint import pprint
from etas.inversion import ETASParameterCalculation

set_up_logger(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    # Invert parameters and save
    forecast_config = 'ch_forecast_config.json'
    etas_invert = ETASParameterCalculation(forecast_config)
    etas_invert.prepare()
    etas_invert.invert()
    etas_invert.store_results('output', store_pij=True, store_distances=True)
    pprint(etas_invert.__dict__)

    # Reload the stored set of parameters.
    parameters_path = 'output/parameters_ch.json'  # as set in forecast_config
    etas_reload = ETASParameterCalculation.load_calculation(
        parameters_path)
    pprint(etas_reload.__dict__)


if __name__ == '__main__':
    main()
