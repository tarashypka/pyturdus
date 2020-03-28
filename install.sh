#!/usr/bin/env bash

MODULE_DIR=$(realpath $(dirname $0))
PYTHON_VERSION=3.7

CONDA_PATH="missing"
ENV_NAME="missing"
HELP_MSG="Usage: install.sh --conda=/path/to/conda --env=env_name"

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
      ENV_NAME=${param#*=}
      shift
      ;;
    --conda=*)
      CONDA_PATH=${param#*=}
      shift
      ;;
    --help)
      echo ${HELP_MSG}
      exit
  esac
done

if [[ ${CONDA_PATH} == "missing" ]]; then
  err "Not found --conda argument!"
fi

if [[ ${ENV_NAME} == "missing" ]]; then
  err "Not found --env argument!"
fi

echo ENV=${ENV_NAME}
echo CONDA=${CONDA_PATH}

export PATH=${CONDA_PATH}/bin:$PATH

ENV_PATH=${CONDA_PATH}/envs/${ENV_NAME}
if [[ ! -d ${ENV_PATH} ]]; then
    echo "Create new environment at ${ENV_PATH} ..."
    conda create -n ${ENV_NAME} python=${PYTHON_VERSION}
    ENV_INSTALLED=1
fi
conda activate ${ENV_NAME}

PIP=${ENV_PATH}/bin/pip

cd ${MODULE_DIR}

${PIP} install -r requirements.txt
