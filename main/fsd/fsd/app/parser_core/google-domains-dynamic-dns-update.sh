#!/bin/bash

### Google Domains provides an API to update a DNS "Syntheitc record". This script
### updates a record with the script-runner's public IP, as resolved using a DNS
### lookup.
###
### Google Dynamic DNS: https://support.google.com/domains/answer/6147083
### Synthetic Records: https://support.google.com/domains/answer/6069273

USERNAME="EDNp7y4tnpwdzGbE"
PASSWORD="NFe6RI16BiQP65pQ"
HOSTNAME="financialstatementdata.com"

# Update Google DNS Record
URL="https://${USERNAME}:${PASSWORD}@domains.google.com/nic/update?hostname=${HOSTNAME}"
curl -s $URL

USERNAME="0z7qgLwFKJWWJpgM"
PASSWORD="fi4G9Q1htVdAsDhA"
HOSTNAME="theivorybasement.com"

URL="https://${USERNAME}:${PASSWORD}@domains.google.com/nic/update?hostname=${HOSTNAME}"
curl -s $URL

USERNAME="aDTZlGppapgVpgaP"
PASSWORD="H9ilgAKU0DuqFdJr"
HOSTNAME="layersofabstraction.io"

URL="https://${USERNAME}:${PASSWORD}@domains.google.com/nic/update?hostname=${HOSTNAME}"
curl -s $URL


USERNAME="KLtuygEKjBsuuGEt"
PASSWORD="x4cgu1FzX3vblJfF"
HOSTNAME="daviddaltonward.com"

URL="https://${USERNAME}:${PASSWORD}@domains.google.com/nic/update?hostname=${HOSTNAME}"
curl -s $URL

