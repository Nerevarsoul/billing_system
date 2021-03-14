#!/bin/bash

set -e

python=`which python`

cd app
alembic upgrade head

exec "$@"
