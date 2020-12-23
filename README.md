# SAMC implemented in Cell-DEVS

See `report/report.pdf` for details

## Usage

`$ python3 ./config_maker.py` to generate or update the input files found in `./config`

`$ cmake . && make` to make, assuming everything is as it should be

`$ python3 ./display_results.py` to run all input files, or `$ python3 ./display_results.py './config/name or glob of input files*' './config/more names or globs of input files*'` to run any number of inputs, in order.

Good luck!
