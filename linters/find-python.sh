#!/usr/bin/env bash

set -e

find apps core home \
	-type d -name migrations -prune -o \
	-type f -name "*.py" \
	-exec "$@" {} +
