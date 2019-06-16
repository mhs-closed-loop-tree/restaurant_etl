error() {
  local parent_lineno="$1"
  local message="$2"
  local code="${3:-1}"
  if [[ -n "$message" ]]; then
    echo $message
  fi
  echo "Near line ${parent_lineno}; exiting with status ${code}"
  exit "${code}"
}

trap 'error ${LINENO}' ERR
