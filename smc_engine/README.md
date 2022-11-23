# Install qrunGenomeSMC

cmake . && make 

Note: ensure there are no CMakeFiles and _deps directories.

# Install runGenomeSMC

make -f makefile_classic

## Known issues

#### fatal error: uuid/uuid.h: No such file or directory

sudo apt-get install uuid-dev
