#!/usr/bin/env bash
#
#  Topology Exporter
#  Copyright © 2022-2025 Barcelona Supercomputing Center (BSC)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#  This work has received funding from the European Union's HORIZON research 
#  and innovation programme under grant agreement No. 101070177.
#
# -*- coding: utf-8 -*-

###########################
# Topology Exporter tests #
###########################

# GLOBAL SETTINGS #

# Topology Exporter refresh interval
export readonly INTERVAL=.1 # must be a multiple of SPF2

# Colours
readonly RED='\e[31m'
readonly GREEN='\e[32m'
readonly BROWN='\e[33m'
readonly BLUE='\e[34m'
readonly RESET='\e[0m'

# Icons
readonly SPIN=(⠋ ⠙ ⠹ ⠸ ⠼ ⠴ ⠦ ⠧ ⠇ ⠏)
readonly WAIT="\e[1A ${BROWN}-${RESET}"
readonly PASS="\e[1A ${GREEN}✔${RESET}"
readonly FAIL="\e[1A ${RED}✘${RESET}"

# Animation
readonly FPS=10 # Frames Per Second
readonly FPS2=$(bc -l <<< "$FPS * 2")
readonly SPF2=$(bc -l <<< "1 / $FPS2")

# Testing values
readonly PODS=(1.1-1 1.2-1 1.2-2 2.1-1 2.1-2 2.1-3) # application.component-replica
readonly T=8 # number of tests
t=0 # current test

# HELPER FUNCTIONS #

ini_header() {
    echo -e "[+] Running ${t}/${T}"
}

upd_header() {
    ((t++))
    echo -e "\e[${t}A[+] Running ${t}/${T}\e[${t}B\r   $1"
}

end_header() {
    ((t++))
    echo -en "\e[${t}A${BLUE}[+] Running ${T}/${T}${RESET}\e[${t}B\r"
}

echo_wait() {
    echo -e ${WAIT/-/${SPIN[$(date +%1N) % ${#SPIN[@]}]}}
}

wait_seconds() {
    # Two iterations per SPF to not skip any frame
    for i in $(seq 1 $(bc -l <<< "$1 * $FPS2"))
    do
        echo_wait
        sleep $SPF2
    done
}

# CORE FUNCTIONS #

#######################################
# Setup Aggregator topology
# Arguments:
#   Topology filename id topologies/aggregator_<id>.json
#######################################
setup_agg() {
    echo_wait
    cp topologies/aggregator_$1.json components/aggregator/aggregator.json
}

#######################################
# Change application monitoring
# Arguments:
#   Application to start monitoring or to end monitoring if negative
#######################################
monitor_app() {
    echo_wait
    if [ ${1:0:1} = '-' ]
    then
        curl -s -o /dev/null -X DELETE localhost/applications/app_instance_${1:1}
    else
        curl -s -o /dev/null localhost/applications/app_instance_$1 --upload-file descriptors/application_$1.yaml
    fi
}

#######################################
# Check if the actual outputs of the applications match the expected ones
# Arguments:
#   Result filename ids results/output_<id>.json of corresponding PODS
#######################################
check_outs() {
    since=$(date -Ins)
    wait_seconds ${INTERVAL}

    for pod in ${PODS[@]}
    do
        expect=$(cat results/output_$1.json)
        actual=$(docker logs --since ${since} -n 1 tests-application_${pod})
        if cmp -s <(jq -S . <(echo $expect)) <(jq -S . <(echo $actual))
        then
            echo_wait
            shift
        else
            echo -e ${FAIL}
            echo -e "=> Output from application_${pod}:"
            echo " - Expect:"
            jq -S . <(echo $expect)
            echo " - Actual:"
            jq -S . <(echo $actual)
            exit 1
        fi
    done

    echo -e ${PASS}
}

# MAIN EXECUTION #

docker compose up --build --wait
trap "docker compose down" EXIT

ini_header

upd_header "Empty topology and no monitoring applications"
setup_agg 0
check_outs '' '' '' '' '' ''

upd_header "Set topology with all application component replicas"
setup_agg 1_2
check_outs '' '' '' '' '' ''

upd_header "Start monitoring application 1"
monitor_app 1
check_outs 1.1 1.2 1.2 '' '' ''

upd_header "Start monitoring application 2"
monitor_app 2
check_outs 1.1 1.2 1.2 2 2 2

upd_header "Stop monitoring application 2"
monitor_app -2
check_outs 1.1 1.2 1.2 '' '' ''

upd_header "Set topology only with application 1 component 1"
setup_agg 1.1
check_outs 1.1 01 01 '' '' ''

upd_header "Add replica 1 of application 1 component 2 to the topology"
setup_agg 1-1
check_outs 1.1 1.2-1 1.2-1 '' '' ''

upd_header "Stop monitoring application 1"
monitor_app -1
check_outs '' '' '' '' '' ''

end_header