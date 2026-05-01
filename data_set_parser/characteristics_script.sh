#!/bin/bash

PROGRAM="./.venv/bin/python main.py"
FOLDER="characters"

MAX_N=10
MAX_M=10

for n in $(seq 1 $MAX_N); do
    for m in $(seq 1 $MAX_M); do
        echo "Running: -cf $n $m"
        $PROGRAM -cf $n $m $FOLDER
    done
done