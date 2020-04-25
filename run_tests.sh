#!/bin/bash

tests=(
    'tests.test_package_init'
    'tests.test_prop'
    'tests.test_abc'
    'tests.test_types'
    'tests.test_version'
    'tests.test_defaults'
    'tests.test_mixins_PropMixin'
    'tests.test_unro'
    'tests.test_utils'
)

print_chars(){
    local how_many=$1
    local which_char=${2:-=}
    for i in $(seq 1 $how_many);do
        printf "$which_char"
    done
    printf "\n"
}

print_msg(){
    local msg=$1
    local c=$((${#msg}+10))
    echo
    print_chars $c
    echo "==== $msg ===="
    print_chars $c

}

for test in "${tests[@]}"; do
    print_msg "python -m $test"
    if ! python -m "$test"; then
        exit $?
    fi
done
