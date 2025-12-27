#!/usr/bin/env bash

start_time=$(date +"%Y-%m-%d %H:%M:%S")
#ansible-playbook  -i inventory/hosts.yml playbooks/continuous_delivery.yml --tags pacific -e "host_group=openEuler_compile_server test_host_group=openEuler_x86_test os_family=openEuler"
ansible-playbook  -i inventory/hosts.yml playbooks/continuous_delivery.yml --tags pacific -e "host_group=kylin_compile_server test_host_group=kylin_x86_test os_family=kylin"
#ansible-playbook  -i inventory/hosts.yml playbooks/continuous_push.yml --tags pacific -e "test_host_group=openEuler_x86_test os_family=openEuler"
end_time=$(date +"%Y-%m-%d %H:%M:%S")
echo "start_time: $start_time"
echo "end_time: $end_time"

exit $?
