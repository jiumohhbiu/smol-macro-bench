#!/bin/bash


apps_dir="./apps"

if [ ! -d "$apps_dir" ]; then
    mkdir -p "$apps_dir"
fi

build_app() {
    apps_dir="./apps"
    IFS=',' read -a arr <<< "$1"
    path="${arr[0]}"
    IFS=' ' read -a builder_options <<< "${arr[1]}"
    IFS=' ' read -a files <<< "${arr[2]}"
    target="${arr[3]}"
    build_exec="${arr[4]}"

    ./"$build_exec" -o "$apps_dir""/""$path $target" -f "${files[@]}" --options "${builder_options[@]}"
}
export -f build_app


if [ $# -lt 1 ]; then
    echo provide apps info path
    exit 1
else
    if [ ! -f "$1" ]; then
        echo provide valid path to apps info
        exit 1
    fi
fi
apps_info_path="$1"

parallel=""
if [ $# -gt 1 ]; then
    if [[ $2 == "-p" || "$2" == "--parallel" ]]; then
        parallel="$2"
    fi
fi

mapfile -t infos < <(cat "$apps_info_path")
if [ -n "$parallel" ]; then
    printf '%s\0' "${infos[@]}" | parallel -0 --jobs=16 build_app
else
    for info in "${infos[@]}"; do
        build_app "$info"
    done
fi

exit 0
