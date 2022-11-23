#!/bin/bash
for number in {0..35}
do
netstat -tulpn | grep SemiHonestYao | awk '{print $7}' | grep -o '[0-9]\+' | xargs kill
done
