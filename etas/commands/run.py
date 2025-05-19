import argparse
import os
import logging
import json
from datetime import datetime, timedelta
import etas
from etas.commands.sim import sim, sim_time_inv
from etas import set_up_logger
from etas.inversion import ETASParameterCalculation
import shutup
shutup.please()

set_up_logger(level=logging.INFO)


def run(config, continuation=True, forecast_duration=None,
        n_sims=None, rates=False, update=False, region='',**kwargs):
    config_dict, sim_fn, fd, ns = parse_args(config,
                                             forecast_duration,
                                             n_sims)
    rates = rates or config_dict.get('rates', False)
    region = region or config_dict.get('region', False)
    update = update or config_dict.get('update', False)

    config_dict = get_prev_sim(config_dict, fd)

    # Invert parameters
    calculation = ETASParameterCalculation(config_dict, **kwargs)
    calculation.prepare()

    subscript = ('_' + str(calculation.id)) * bool(calculation.id)
    parameters = os.path.join(calculation.data_path,
                              f'parameters{subscript}.json')

    if update or (not os.path.exists(parameters)):
        calculation.invert()
        calculation.store_results()

    # Simulate
    if continuation:
        if rates is False:
            sim(parameters, output_fn=sim_fn, rates=False,
                forecast_duration=fd, n_sims=ns, **kwargs, fmt='csep')
        else:
            sim(parameters, output_fn=sim_fn, rates=True, region=region,
                forecast_duration=fd, n_sims=ns, **kwargs, fmt='csep')
    else:
        sim_time_inv(parameters)


def get_prev_sim(config_dict, fd):
    start = config_dict['start_date']
    datapath = config_dict['data_path']
    id_ = config_dict.get('id', 'id')

    params_path = os.path.join(datapath, f'parameters_{id_}.json')
    if os.path.isfile(params_path):
        with open(params_path, 'r') as f:
            prev_params = json.load(f)
        prev_start = datetime.fromisoformat(start) - timedelta(fd)
        if prev_start == prev_params['timewindow_end']:
            config_dict['theta_0'] = prev_params['theta']

    return config_dict


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
    parser.add_argument('-c', '--continuation',
                        help='Time invariant or dependent forecast.'
                             'i.e. Continues previous sequences', type=bool)

    args = parser.parse_args()
    run(**vars(args))


if __name__ == '__main__':
    main()
