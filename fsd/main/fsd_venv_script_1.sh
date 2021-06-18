#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

source "${DIR}/fsd/bin/activate"

python3 "${DIR}/fsd/fsd/app/update_company_html_table.py"
