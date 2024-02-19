#!/bin/bash

# Initialize failure counters
pull_failures=0
checkout_failures=0
exclude_list=()

# Function to report pull failure in red
report_pull_failure() {
    echo -e "\033[31mFailed to pull latest changes for $1!\033[0m"
    pull_failures=$((pull_failures+1))
}

# Function to report checkout failure in red
report_checkout_failure() {
    echo -e "\033[31mFailed to switch branch for $1!\033[0m"
    checkout_failures=$((checkout_failures+1))
}

# Parse command-line options for exclude argument
while getopts "e:" opt; do
    case "$opt" in
        e) IFS=',' read -ra exclude_list <<< "$OPTARG" ;;
        *) echo "Usage: $0 [-e 'submodule1,submodule2,...']" && exit 1 ;;
    esac
done

# Extract submodule information from .gitmodules file and process each submodule
while IFS= read -r line; do
    if [[ "$line" =~ \[submodule ]]; then
        read -r path_line
        read -r url_line
        read -r branch_line

        # Extract submodule path and branch
        submodule_path=$(echo "$path_line" | sed 's/.*= //')
        submodule_branch=$(echo "$branch_line" | sed 's/.*= //')

        # Check if submodule should be skipped
        skip=0
        for exclude in "${exclude_list[@]}"; do
            if [[ "$submodule_path" == "$exclude" ]]; then
                skip=1
                break
            fi
        done
        if [[ $skip -eq 1 ]]; then
            continue
        fi

        # Go to submodule directory
        pushd "$submodule_path" > /dev/null

        # Get the current branch of the submodule
        current_branch=$(git rev-parse --abbrev-ref HEAD)

        # If current branch doesn't match with branch in .gitmodules, switch to that branch
        if [[ "$current_branch" != "$submodule_branch" ]]; then
            echo "Switching $submodule_path from $current_branch to $submodule_branch..."
            git checkout "$submodule_branch"
            if [[ $? -ne 0 ]]; then
                report_checkout_failure "$submodule_path"
                # Go back to the main repo directory and continue with the next submodule
                popd > /dev/null
                continue
            fi
        fi

        # Pull the latest changes and check for success
        echo "Pulling latest changes for $submodule_path..."
        git pull
        if [[ $? -ne 0 ]]; then
            report_pull_failure "$submodule_path"
        fi

        # Go back to the main repo directory
        popd > /dev/null
    fi
done < .gitmodules

# Report total number of failures at the end
if [[ $checkout_failures -eq 0 ]]; then
    echo -e "\033[32mCheckout Failures: $checkout_failures\033[0m"
else
    echo -e "\033[31mCheckout Failures: $checkout_failures\033[0m"
fi

if [[ $pull_failures -eq 0 ]]; then
    echo -e "\033[32mPull Failures: $pull_failures\033[0m"
else
    echo -e "\033[31mPull Failures: $pull_failures\033[0m"
fi

echo "Finished updating submodules!"
