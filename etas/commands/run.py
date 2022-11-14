import argparse
import os
import logging
from etas.commands.sim import sim, sim_time_inv
from etas import set_up_logger
from etas.inversion import ETASParameterCalculation

set_up_logger(level=logging.DEBUG)


def run(config, output_fn='simulation.csv', continuation=True,
        parameters=False, forecast_duration=30, n_sims=100, **kwargs):
    if parameters:
        print(parameters)
        calculation = ETASParameterCalculation.load_calculation(parameters)
    else:
        calculation = ETASParameterCalculation(config, **kwargs)
        calculation.prepare()
        calculation.invert()
        calculation.store_results()

        subscript = ('_' + str(calculation.id)) * bool(calculation.id)
        parameters = os.path.join(calculation.data_path,
                                  f'parameters{subscript}.json')
    if continuation:
        sim(parameters, output_fn=output_fn,
            forecast_duration=forecast_duration, n_sims=n_sims, **kwargs)
    else:
        sim_time_inv(parameters)


def main():
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
    parser.add_argument('config', help='Configuration file or parameter file'
                                       ' of the simulation', type=str)
    parser.add_argument('-o', '--output_fn', help='Output filename', type=str)
    parser.add_argument('-c', '--continuation',
                        help='Time invariant or dependent forecast.'
                             'i.e. Continues previous sequences', type=bool)
    parser.add_argument('-p', '--parameters',
                        help='Previously estimated parameters file', type=str)

    args = parser.parse_args()
    run(**vars(args))


if __name__ == '__main__':
    main()
