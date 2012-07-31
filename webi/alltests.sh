#!/bin/bash

# sh -c is mandatory to have basename working after the substitution of {}
find features/ \( ! -name wizard.feature -a -name '*.feature' \) -exec sh -c 'PYTHONPATH=.. lettuce --with-xunit --verbosity=4 {} --xunit-file=$PWD/$(basename {} .feature).xml' \;
