import os

def missing_cert():
    return not os.path.exists('pyeric/instances/blueprint/cert.pfx')

def missing_pyeric_lib():
    return not os.path.exists('pyeric/lib/libericapi.so')