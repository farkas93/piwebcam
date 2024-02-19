#!/bin/bash

# An array to hold excluded submodule names
declare -a excluded

# Parse the arguments
while getopts "e:" opt; do
    case $opt in
        e)
            IFS=',' read -ra ADDR <<< "$OPTARG"
            for i in "${ADDR[@]}"; do
                excluded+=("$i")
            done
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

# Function to check if a submodule is in the excluded list
is_excluded() {
    local name="$1"
    for ex in "${excluded[@]}"; do
        if [[ "$ex" == "$name" ]]; then
            return 0
        fi
    done
    return 1
}

# Go through each submodule in .gitmodules and check out if it's not in the excluded list
while IFS= read -r line; do
    if [[ $line =~ \[submodule\ \"(.*)\"\] ]]; then
        name="${BASH_REMATCH[1]}"
        if ! is_excluded "$name"; then
            git submodule update --init "${name}"
        fi
    fi
done < .gitmodules
