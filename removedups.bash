#!/bin/bash
for file in *.csv
do
    python3 removedups.py "$file" "nodups/$file"
done 