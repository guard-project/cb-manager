#!/bin/sh
# Copyright (c) 2020 GUARD

watchmedo auto-restart --patterns="*.py;*.yaml" --recursive bash -- scripts/start.sh $*
