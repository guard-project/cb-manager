#!/bin/sh
# Copyright (c) 2020 GUARD

if [ -z "$1" ]; then
    python main.py
else
    # ItalTel ElasticSearch endpoint: http://guard3.westeurope.cloudapp.azure.com:9200
    if [ "$1" = "italtel" ]; then
        python main.py --es-endpoint http://guard3.westeurope.cloudapp.azure.com:9200
    else
        echo "Error: ElasticSearch endpoint unknown"
    fi
fi

