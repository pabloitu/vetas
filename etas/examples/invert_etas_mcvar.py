import json
import logging
from pprint import pprint
from etas import set_up_logger
from etas.inversion import ETASParameterCalculation
set_up_logger(level=logging.DEBUG)

'''
Inverts ETAS parameters with varying magnitude of completeness
        Config file for this example is in 'artifacts/invert_etas_mc_var_config.json'
        The configuration attributes are identical to the example inver_etas.py.

    WHEN RUNNING ETAS INVERSION WITH VARYING MC:
        "mc" needs to be set to "var" in the config data file in
        'artifacts/invert_etas_mc_var_config.json', whereas the input catalog pointed in
        "fn_catalog" needs to have an "mc_current" column (example
        described below). Also, a reference magnitude "m_ref" needs to be
        provided. This could be, although not required, the minimum mc_current.

        The file 'example_catalog_mc_var.csv; contains an example synthetic catalog that
        has an additional column named "mc_current",
        which for each event contains the completeness magnitude (mc) valid
        at the time and location of the event.
        in Sothern California (latitude < 37),
            mc = 3.0 if time <= 1981/1/1,
                 2.7 if 1981/1/1 < time <= 2010/1/1
                 2.5 if time > 2010/1/1
        in Northern California (latitude >= 37),
            mc = 3.1 if time <= 1981/1/1,
                 2.8 if 1981/1/1 < time <= 2010/1/1
                 2.6 if time > 2010/1/1
        this is an example of space-time varying mc, and is not intended to
        reflect reality.
'''


def main():
    with open("artifacts/invert_etas_mc_var_config.json", 'r') as f:
        inversion_config = json.load(f)

    calculation = ETASParameterCalculation(inversion_config)
    calculation.prepare()
    parameters = calculation.invert()
    calculation.store_results(inversion_config['data_path'])
    pprint('Final parameters\n', parameters)


if __name__ == '__main__':
    main()
