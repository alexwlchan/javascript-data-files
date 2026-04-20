#!/usr/bin/env bash

set -o errexit
set -o nounset

# Print a command in blue, then run the command
run_command() {
    echo ""
    echo -e "\033[34m-> $@\033[0m"
    bash -c "$@"
}

run_command 'ruff format'

if [[ "${CI:-}" == "true" ]]
then
  run_command 'git diff --exit-code'
fi

run_command 'ruff check'
run_command 'ty check'
run_command "coverage run -m pytest tests"
run_command "coverage report"
