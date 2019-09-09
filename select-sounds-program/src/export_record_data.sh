#!/usr/bin/env bash

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

USERNAME=${1:-'username'}
PASSWORD=${2:-'password'}
DB=${3:-'selectsoundsdb'}
FIELDS=${4:-'name,artist,label,country,release_date,speed,tracklist'}
FILE_NAME=${5:-'records.csv'}

# TESTING
#echo "mongoexport --host TestCluster-shard-0/testcluster-shard-00-00-9feub.azure.mongodb.net:27017,testcluster-shard-00-01-9feub.azure.mongodb.net:27017,testcluster-shard-00-02-9feub.azure.mongodb.net:27017 --ssl --username ${USERNAME} --password ${PASSWORD} --authenticationDatabase admin --db ${DB} --collection records --type=csv --fields ${FIELDS} --out ${CWD}/data/${FILE_NAME}"

# Command will fail without passing username + password as parameters when calling command

mongoexport --host TestCluster-shard-0/testcluster-shard-00-00-9feub.azure.mongodb.net:27017,testcluster-shard-00-01-9feub.azure.mongodb.net:27017,testcluster-shard-00-02-9feub.azure.mongodb.net:27017 --ssl --username ${USERNAME} --password ${PASSWORD} --authenticationDatabase admin --db ${DB} --collection records --type=csv --fields ${FIELDS} --out ${CWD}/data/${FILE_NAME}