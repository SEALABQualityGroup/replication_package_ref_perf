#!/bin/bash
# Find Github repositories having a pom.xml with a jmh-core dependency

if [[ $# -eq 0 ]]; then
  echo "Usage: $0 username:token"
  exit 0
fi

URL="https://api.github.com/search/code?per_page=100&q="
QUERY="jmh-core+in:file+filename:pom.xml+language:maven"
AUTH=$1
PAGE=1

while true
do
    repos=$(curl -u $AUTH -s -H "Accept: application/vnd.github.mercy-preview+json" "${URL}${QUERY}&page=${PAGE}" | grep '^        "html_url"' | uniq | cut -d\" -f4)
    echo "$repos"
    [[ $(echo "$repos" | wc -l) -gt 1 ]] || break
    ((PAGE++))
    sleep 5
done
