# Quantum private phylogenetic analysis

An application that securely computes phylogenetic trees based on the PHYLIP package, secure multiparty computation and quantum technologies. It is based on the [QSHY](https://github.com/manel1874/QSHY/tree/dev-cq-phylip) framework.


## Requirements

The application runs on Linux (x64 only, 32 bit systems are not supported) and has been tested on the following version:

- Ubuntu 16.04/18.04 LTS

To run the application one must have python3.5 or higher PyQt5 and flask and also configure the ip of the machine in the config.txt file.

- Install PyQt5 Linux:
```
sudo apt-get install python3-pyqt5
````

- Install PyQt5 windows:
-pip install pyqt5

- Install flask:
```
pip3 install flask
```

- Install all the dependencies required for the SMC system:
```
./install.sh
sudo apt-get install uuid-dev
```

- In the `smc_engine` folder install the quantum and the classical system
```
cd smc_engine
cmake && make
make -f makefile_classic
```
Note: ensure there are no CMakeFiles and _deps directories.



## How to run:

Note 1: This application depends on a key management system that provides two types of keys (oblivious keys and symmetric keys). We can provide it upon request.

Note 2: This application is supposed to be used by different parties located at different computers. Therefore, these instructions are supposed to be applied for every party that wants to join in a private computation.

- Open two terminals.

- In one terminal, fire the key management system from its corresponding folder:
```
python3 run_lkms.py
``

- In the other terminal, fire the application:
```
./launch_app_and_server.sh
```

## Demo

You can watch a demo of the application in [this](https://www.youtube.com/watch?v=gPAPgZYbd8E) YouTube video.

## Resources

This project is based on the following papers:

- [Private Computation of Phylogenetic Trees based on Quantum Technologies](https://ieeexplore.ieee.org/document/9732453), IEEE Access, 2022.
- [Quantum Secure Multiparty Computation of Phylogenetic Trees of SARS-CoV-2 Genomes](https://ieeexplore.ieee.org/document/9435479), ConfTELE, 2021.

A presentation of the system can also be seen in [this](https://youtu.be/k_W8_pxNQm8) YouTube video


