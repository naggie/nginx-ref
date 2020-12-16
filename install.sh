#!/usr/bin/env bash

# for Ubuntu 20.04+

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

set -e
cd $(dirname $0)

apt-get install -y nginx certbot

cp nginx.conf /etc/nginx/nginx.conf

