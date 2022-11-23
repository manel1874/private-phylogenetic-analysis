#!/bin/sh

USERNAME=$(whoami)

/home/$USERNAME/MPC-Benchmark/SemiHonestYao/SemiHonestYao -partyID $1 -configFile $2 -partiesFile $3 -internalIterationsNumber 1
