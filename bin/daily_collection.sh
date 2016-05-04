#!/bin/bash

cd ~/hdx-monitor-funnel-stats

for i in `seq 1 2`;
do
    echo "Running: $i out of 2"
    source venv/bin/activate
    python scripts/setup/
done
