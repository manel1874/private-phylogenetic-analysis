#!/bin/bash
for number in {0..99}
do
awk 'END{print NR}' b_Sequence_"$number".txt
echo $number
done
