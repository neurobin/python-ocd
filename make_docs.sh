#!/bin/bash

docs=(
    'ocd'
    # 'ocd.abc'
    # 'ocd.defaults'
    # 'ocd.deprecate'
    # 'ocd.mixins'
    # 'ocd.prop'
    # 'ocd.types'
    # 'ocd.unro'
    # 'ocd.utils'
    # 'ocd.version'
    # 'ocd.warnings'
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

for doc in "${docs[@]}"; do
    print_msg "pdoc3 '$doc' --html --force"
    pdoc3 --html --force "$doc"
done
