#!/usr/bin/env bash

# for Ubuntu 20.04+

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

set -e
cd $(dirname $0)

apt-get install -y nginx certbot openssl

cp nginx.conf /etc/nginx/nginx.conf

mkdir -p /etc/nginx/include
cp include/* /etc/nginx/include/

if [ ! -f /etc/nginx/dhparams.pem ]; then
    openssl dhparam -out /etc/nginx/dhparams.pem 2048
fi

systemctl reload nginx
