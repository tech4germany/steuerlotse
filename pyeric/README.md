# Required steps before using PyEric 1/2

PyEric is just a wrapper around ERiC. For this to work you will need to download the latest ERiC library and place the required library files in a `lib` folder.

 - Download `ERiC-32.2.4.0-Linux-x86_64.jar` from the [ELSTER developer portal](https://www.elster.de/elsterweb/infoseite/entwickler).
 - Place the following files into a `lib` folder in _this directory_ such that it matches the given structure:

```
pyeric$ tree lib
lib
├── libericapi.so
├── libericxerces.so
├── libeSigner.so
└── plugins2
    ├── libcheckESt_2011.so
    ├── libcheckESt_2019.so
    └── libcommonData.so
```

# Required steps before using PyEric 2/2

You also need to acquire a test certificate from ELSTER and place it under `pyeric/instances/blueprint/cert.pfx`.


# Tests

All unittests that require the ERiC library or `cert.pfx` will be skipped if it is missing.