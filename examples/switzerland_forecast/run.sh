#/bin/sh

# Run inversion and simulation, by continuating the observed catalog
etas-run ch_forecast_config.json -o simulation.csv

# Run simulation using stored parameters in previous inversion
etas-run ch_forecast_config.json -p output/parameters_ch.json -o simulation.csv

# Run simulation using stored parameters, and no continuation (fresh start using burning period)
etas-run ch_forecast_config.json -p output/parameters_ch.json -o simulation.csv -c False