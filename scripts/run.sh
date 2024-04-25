#!/bin/bash
# Can be called with ./scripts/run.sh [host:port]

if [ "$1" == "runserver" ]; then
  shift
fi

runserverArgs=()

for arg
do
  runserverArgs+=("$arg")
done

function cleanup() {
  # kills all the captured PIDs, then exits
  if [ -n "$P1" ]; then
    kill -9 $P1
  fi
  if [ -n "$P2" ]; then
    kill $P2
  fi
  exit 0
}

function restart_django() {
  echo "restarting django."
  if [ -n "$P2" ]; then
    kill $P2
  fi
  python3 -u manage.py runserver ${runserverArgs[@]} &
  P2=$!
}

# trap ctrl-c and call cleanup()
trap cleanup EXIT

npm run dev &
P1=$!
python3 -u manage.py runserver ${runserverArgs[@]} &
P2=$!

sleep 2

# keep the script idle until ctrl-c is received
while true
do
  echo "type:"
  echo "- \"d\" to restart django"
  echo "- \"e\" or Ctrl-c to exit"
  read -r line
  if [ "$line" = "d" ]; then
    restart_django
  elif [ "$line" = "e" ]; then
    cleanup
  fi
  sleep 2
done
