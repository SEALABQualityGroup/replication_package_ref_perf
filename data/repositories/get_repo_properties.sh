#!/bin/bash
# Get a set of properties from a given Github repository

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 username:token repository property1,property2,..."
  echo "Example: ./get_repo_properties.sh mtucci:token openzipkin/brave stargazers_count,fork"
  exit 0
fi

REPO=$2
REPO_URL="https://api.github.com/repos/$2"
AUTH=$1
PROPS=$3

json=$(curl -u $AUTH -s $REPO_URL)

for i in ${PROPS//,/ };do echo "$json" | grep "^  \"$i\"" | tr ',' ' '; done
