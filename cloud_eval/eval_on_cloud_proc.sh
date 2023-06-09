#!/bin/sh
set -e

# Load env params from env file
# expecting these env vars to be set
# MODEL_NAME
# MODEL_TYPE_ID
source ./cloud_eval/.cloud_eval_env

# create dir for log/tracing files related to cloud evaluation
mkdir -p tmp

if [ $MODEL_TYPE_ID == "-1" ]; then
  echo "Find out and fill in your model type id in [./cloud_eval/.cloud_eval_env] . You can obtain the model type id from DSP (or ask the DSP Team)"
  exit 9
fi


# params validation
if [ "$1" != "" ]; then
  VERSION="$1"
else
  echo Please provide a version name
  exit 9
fi

if [ "$2" != "" ]; then
  DATASET="$2"
else
  echo "Please provide a dataset name (i.e [1600_sig_valid.csv])"
  exit 9
fi

if [ "$3" == "stg" ]; then
  echo "Setting DSP env to staging"
  DSP_ENV="stg"
  STEPFUNCTION_STATE_MACHINE="arn:aws:states:us-east-2:769057607614:stateMachine:DS_IL_Model_Evaluation_Full_Batch_Staging"
else
  echo "Setting DSP env to production"
  DSP_ENV="prd"
  STEPFUNCTION_STATE_MACHINE="arn:aws:states:us-east-2:769057607614:stateMachine:DS_IL_Model_Evaluation_Full_Batch"
fi

DESCRIPTION="version ${VERSION}"
GIT_REPO=$(git config --get remote.origin.url | sed 's/.*\/\([^ ]*\/[^.]*\).*/\1/')


if [ "${SKIP_WORKAROUNDS}" != "TRUE" ]; then
  cloud_eval/tag_version.sh "${VERSION}" "${DESCRIPTION}"
fi

STEPFUNCTION_INPUT='{"env": "'${DSP_ENV}'", "model": {"name": "'${MODEL_NAME}'", "version": "'${VERSION}'", "type_id": "'${MODEL_TYPE_ID}'", "repo": "'${GIT_REPO}'"}, "dataset": { "name": "'${DATASET}'" }}'
echo starting evalutation flow...
aws stepfunctions start-execution --region us-east-2 --state-machine-arn "${STEPFUNCTION_STATE_MACHINE}" --input "$STEPFUNCTION_INPUT" > ./tmp/exec_eval.json
echo "Simulation is underway with ${STEPFUNCTION_INPUT}. Execution details in ./tmp/exec_eval.json"
