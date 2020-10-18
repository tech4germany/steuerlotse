#!/bin/bash
find app -type d -name __pycache__ -exec rm -r {} \;;
find pyeric -type d -name __pycache__ -exec rm -r {} \;;
find tests -type d -name __pycache__ -exec rm -r {} \;;
rm -r pyeric/instances/session_*;