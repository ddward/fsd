#!/bin/bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


source "${DIR}/api/bin/activate"

cd "${DIR}/api/api"

python3 -m gui.company_list_update

cd $DIR
deactivate
