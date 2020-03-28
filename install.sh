#!/usr/bin/env bash

MODULE_DIR=$(realpath $(dirname $0))

ENV_PATH="missing"
HELP_MSG="Usage: install.sh --env=/path/to/python/env"

err() {
    echo
    echo ${1}
    echo
    echo ${HELP_MSG}
    echo
    exit
}

for param in $@; do
  case ${param} in
    --env=*)
      ENV_PATH=${param#*=}
      shift
      ;;
    --help)
      echo ${HELP_MSG}
      exit
  esac
done

if [[ ${ENV_PATH} == "missing" ]]; then
  err "Not found --env argument!"
fi

${ENV_PATH}/bin/pip install -r ${MODULE_DIR}/requirements.txt
