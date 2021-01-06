#!/usr/bin/env bash

# for Ubuntu 20.04+, clean instal

if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

function purge {
    pushd /etc/nginx >/dev/null
        for file in "$@"; do
            [ -e $file ] && rm -rf $file
        done
    popd >/dev/null
}

set -e
cd $(dirname $0)

# deps
apt-get install -y nginx certbot python3-certbot-nginx openssl

# remove specific files which are made redundant by this script
purge {sites,modules}-{enabled,available}
purge snippets/fastcgi-php.conf
purge snippets/snakeoil.conf
purge fastcgi.conf
purge koi-win koi-utf win-utf
purge mime.types
purge proxy_params scgi_params uwsgi_params fastcgi_params

# replace main config
cp nginx.conf /etc/nginx/nginx.conf

# ensure important directories exist
mkdir -p /etc/nginx/snippets
mkdir -p /etc/nginx/conf.d

# error pages
mkdir -p /etc/nginx/error-pages/
cp error-pages/* /etc/nginx/error-pages/
chown -R www-data /etc/nginx/error-pages/

# templates, proxy settings, short-hand ssl stuff
cp snippets/* /etc/nginx/snippets/

# required for DH based key exchange
if [ ! -f /etc/nginx/dhparams.pem ]; then
    openssl dhparam -out /etc/nginx/dhparams.pem 2048
fi

systemctl reload nginx

sudo python3 initialise-certbot.py
