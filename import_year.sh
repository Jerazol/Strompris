#!/bin/bash

for m in $(seq 1 12)
do
  for d in $(seq 1 31)
  do
    cmd=$(printf "./import.py -d 2021-%0*d-%0*d\n" 2 $m 2 $d)
    $cmd
    WAITTIME=$(( RANDOM % 10 ))
    echo $WAITTIME
    sleep $WAITTIME
  done
done
