#! /usr/bin/env bash

# {x86-64,arm,arm64,x86}


function gen() {
    python3 generate-json.py $1 -o $2
}


gen x86-64 syscalls_x86-64.json
gen arm syscalls_arm.json
gen arm64 syscalls_arm64.json
gen x86 syscalls_x86.json
