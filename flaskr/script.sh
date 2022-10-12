#!/bin/bash

for var in "$@"
do
    python3 powerPlants.py user changeFinance "$var" 2000
done
