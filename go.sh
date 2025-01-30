#!/bin/bash

config="config.json"
processed="preprocessed.json"
apps_info_path="apps_info.txt"
points_to_sample="points_to_sample.txt"

parallel=""
if [ $# -gt 0 ]; then
    if [[ $1 == "-p" || "$1" == "--parallel" ]]; then
        parallel="$1"
    fi
fi

if ! ./json_preprocesser.py -i "$config" -o "$processed"; then
    exit 1
fi
echo "preprocessed"

if ! ./get_apps.py -i "$processed" > "$apps_info_path"; then
    exit 2
fi
echo "constructed configs"

if ! ./build_apps.sh "$apps_info_path" "$parallel"; then
    exit 3
fi
echo "built apps"

./points_to_sample.py -i "$processed" --apps "$apps_info_path" -o "$points_to_sample"
while : ; do
    [[ -s "$points_to_sample" ]] || break
    if ! ./points_to_sample.py -i "$processed" --apps "$points_to_sample" -o "$points_to_sample"; then
        exit 4
    fi

    if ! ./update_data.sh "$points_to_sample"; then
        exit 5
    fi
done

exit 0
