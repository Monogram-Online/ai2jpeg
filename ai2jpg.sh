#!/usr/bin/bash

createsvg() {
  local d
  local svg
  for d in "./input/"*.ai "./input/"*.AI; do
    jpg=$(echo "$d" | sed 's/.ai//I')
    echo "creating $jpg ..."
    pdftocairo -singlefile -jpeg "$d" $(echo "$jpg" | sed 's/input/output/I')
  done
}

if [ "$1" != "" ];then
  cd $1
fi

createsvg
