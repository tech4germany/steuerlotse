#!/bin/sh
set -ex

service pcscd start

# Hand off to the CMD
exec pipenv run "$@"
