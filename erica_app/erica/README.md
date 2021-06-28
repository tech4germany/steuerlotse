# Required steps before using Erica 1/2
Erica uses Pyeric. Pyeric is just a wrapper around ERiC. For this to work you will need to download the latest ERiC 
library and place the required library files in a `lib` folder.

 - Set the environment variable `ERICA_ENV` to `testing`, `development` or similar.
 - Download `ERiC-32.2.4.0-Linux-x86_64.jar` (or a newer version) from the [ELSTER developer portal](https://www.elster.de/elsterweb/infoseite/entwickler).
 - Place the following files into a `lib` folder in _this directory_ such that it matches the given structure:

```
pyeric$ tree lib
lib
├── libericapi.so
├── libericxerces.so
├── libeSigner.so
└── plugins2
    ├── libcheckElsterDatenabholung.so
    ├── libcheckESt_2020.so
    ├── libcheckVaSt.so
    └── libcommonData.so
````

_NOTE_: If you use a Mac, get the corresponding `*.dylib` files

# Required steps before using Erica 2/2

You also need to acquire a test certificate from ELSTER and place it under `erica/instances/blueprint/cert.pfx`.


# Tests

All unittests that require the ERiC library or `cert.pfx` will be skipped if it is missing.
