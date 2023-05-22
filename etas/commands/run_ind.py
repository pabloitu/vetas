import argparse
import os
import logging
import json
import time
from datetime import datetime, timedelta
import etas
from etas.commands.sim import sim, sim_time_inv
from etas import set_up_logger
from etas.inversion import ETASParameterCalculation
import shutup

shutup.please()

set_up_logger(level=logging.WARN)
logger = logging.getLogger(__name__)


def run_ind(config, forecast_duration=None,
            n_sims=None, **kwargs):
    config_dict, sim_fn, fd, ns = parse_args(config,
                                             forecast_duration,
                                             n_sims)

    # Invert parameters
    logger.warning('Loading Inversion')
    calculation = ETASParameterCalculation.load_calculation(
        config_dict)
    calculation.store_results()

    # Store parameters
    subscript = ('_' + str(calculation.id)) * bool(calculation.id)
    parameters = os.path.join(calculation.data_path,
                              f'parameters{subscript}.json')

    # Simulate
    start = time.perf_counter()
    logger.warning(f'Simulating {ns} catalogs')
    sim(parameters, output_fn=sim_fn,
        forecast_duration=fd, n_sims=ns, **kwargs, fmt='csep')
    logger.warning(f'Finished {ns} catalogs in '
                   f'{time.perf_counter() - start:.1f} seconds')


def parse_args(config, fduration, nsims):
    with open(config, 'r') as f:
        config_dict = json.load(f)

    # Parse Experiment arguments
    if 'start_date' in config_dict.keys():
        start_date = datetime.fromisoformat(config_dict['start_date'])
        end_date = datetime.fromisoformat(config_dict['end_date'])
        # Re-build own Model arguments
        config_dict['forecast_duration'] = (end_date - start_date).days
        fd = config_dict['forecast_duration']
        config_dict['timewindow_end'] = start_date.__str__()
        # Set output forecast path and name to experiment convention
        sim_folder = os.path.join(etas.__path__[0], '..', 'forecasts')
        sim_fn = os.path.join(
            sim_folder,
            f'etas_{start_date.date().isoformat()}_{end_date.date().isoformat()}.csv'
        )
    else:
        sim_fn = 'simulation.csv'
        config_dict['forecast_duration'] = config_dict.get('forecast_duration',
                                                           fduration)
        fd = config_dict['forecast_duration']

    if nsims:
        config_dict["n_simulations"] = nsims
    elif 'n_sims' in config_dict.keys():
        config_dict["n_simulations"] = config_dict["n_sims"]
        nsims = config_dict["n_sims"]
    else:
        nsims = config_dict["n_simulations"]

    # Modify input/state paths relative to config file
    config_dir = os.path.dirname(config)
    if config_dict["shape_coords"].endswith('npy'):
        config_dict["shape_coords"] = os.path.join(config_dir,
                                                   config_dict["shape_coords"])

    config_dict["data_path"] = os.path.join(config_dir,
                                            config_dict["data_path"])
    config_dict["fn_catalog"] = os.path.join(config_dir,
                                             config_dict["fn_catalog"])
    return config_dict, sim_fn, fd, nsims


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('config', help='Configuration file or parameter file'
                                       ' of the simulation', type=str)
    parser.add_argument('-o', '--output_fn', help='Output filename', type=str)
    args = parser.parse_args()
    run_ind(**vars(args))


if __name__ == '__main__':
    main()
