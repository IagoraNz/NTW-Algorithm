#!/bin/sh
set -e

if [ -z "$rtr_ip" ]; then
    echo "A variável rtr_ip não está definida!"
    exit 1
fi

echo "$rtr_ip"

ip route del default && ip route add default via $rtr_ip && python router.py