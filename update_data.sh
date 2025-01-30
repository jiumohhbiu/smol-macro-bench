#!/bin/bash

run_app() {
    apps_dir="./apps"
    IFS=',' read -a arr <<< "$1"
    path="${arr[0]}"
    IFS=' ' read -a builder_options <<< "${arr[1]}"
    files="${arr[2]}"
    target="${arr[3]}"
    build_exec="${arr[4]}"

    dir_path="$apps_dir"/"$path"

    data_dir="./data"
    if [ ! -d "$data_dir" ]; then
        mkdir -p "$data_dir"
    fi

    echo "$path" | ./"$dir_path $target" >> ./data/"$path".txt
}

if [ $# -lt 1 ]; then
    echo provide apps info path
    exit 1
else
    if [ ! -f "$1" ]; then
        echo provide valid path to apps info
        exit 1
    fi
fi
mapfile -t infos < <(cat "$1")

i=0
for info in "${infos[@]}"; do
    echo -e -n $(tput el)updating \["$i"\/"${#infos[@]}"\] "\r"
    run_app "$info"
    i=$(( i + 1 ))
done
echo -e -n $(tput el)

exit 0
