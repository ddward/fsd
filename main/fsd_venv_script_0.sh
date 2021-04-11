#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


source "${DIR}/fsd/bin/activate"

python3 "${DIR}/fsd/fsd/app/full_daily_update.py"


