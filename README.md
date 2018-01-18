# Mousejack-dump-replay

Based on [mousejack-tools](https://github.com/BastilleResearch/nrf-research-firmware)

## Install
  1. Clone [mousejack-tools](https://github.com/BastilleResearch/nrf-research-firmware)
  2. Copy `nrf24-dump.py` and `nrf24-replay.py` to `nrf-research-firmware/tools/`

## Usage

### nrf24-dump.py

Dump wireless data to file

    python ./tools/nrf24-dump.py -a [address]

Example

    python ./tools/nrf24-dump.py -a C0:DE:DE:AD:BE:EF

Dump data will save in `[address].json`

### nrf24-replay.py

Load dump file and make replay attack

    python ./tools/nrf24-replay.py -f [Dump File.json]

Example

     python ./tools/nrf24-replay.py -f C0-DE-DE-AD-BE-EF.json


