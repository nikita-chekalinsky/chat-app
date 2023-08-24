#!/usr/bin/env bash

docker run --name scylla \
 -v ./scylla.yaml:/etc/scylla/scylla.yaml \
 -p 9042:9042 -p 7001:7000 -p 9160:9160 -p 10000:10000 \
 -d scylladb/scylla
 

sleep 30
pip install scylla-driver
python scylla_init.py
