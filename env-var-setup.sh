#!/bin/sh

# ==========================================================================
# Setup script for installing project dependencies.
# NOTE: Run this script while in the project root directory.
#       It will not run correctly when run from another directory.
# ==========================================================================

# Set script to exit on any errors.
set -e

ENVVAR_SAMPLE=.env_SAMPLE
ENVVAR=.env

# Copy and activate sample environment variables, if not already done.
if [ ! -f $ENVVAR ]; then
  echo 'Setting default environment variables...'
  cp -a $ENVVAR_SAMPLE $ENVVAR
fi

source $ENVVAR
echo "Environment variables from $ENVVAR activated."
