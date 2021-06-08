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
apt-get update
apt-get install -y nginx certbot python3-certbot-nginx openssl rename

# remove specific files which are made redundant by this script
purge {sites,modules}-{enabled,available}
purge snippets/fastcgi-php.conf
purge snippets/snakeoil.conf
purge fastcgi.conf
purge koi-win koi-utf win-utf
purge mime.types
purge proxy_params scgi_params uwsgi_params fastcgi_params

# if user or PID has to change, nginx needs to be stopped. It will be started
# later on.
if ! grep -q 'user www-data' /etc/nginx/nginx.conf || ! grep -q '/run/nginx.pid' /etc/nginx/nginx.conf; then
    sudo systemctl stop nginx
fi

# replace main config
cp nginx.conf /etc/nginx/nginx.conf

# ensure permissions are right (if installing over the mattermost-omnibus this
# is necessary as `nginx` user is used)
chown -R www-data /var/{cache,log}/nginx || true

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

# if nginx is not started:
# get nginx started in a minimal state without loading any site config so that
# certbot can proceed
# Nginx may not be started if deliberately stopped due changing pid or user, see above.
sudo rename s/.conf$/.conf.disabled/g /etc/nginx/conf.d/*.conf
sudo service nginx start
sudo rename s/.conf.disabled$/.conf/g /etc/nginx/conf.d/*.conf.disabled

# remove any dangling config files left over if initialise-certbot previously
# failed. Note that the config files should be copied over entirely before
# running this script; that way config files will not be lost.
sudo rm /etc/nginx/conf.d/*.conf.disabled 2> /dev/null || true

# note certbot may attempt to reload nginx
sudo python3 initialise-certbot.py
systemctl reload nginx

# reloading can silently fail, check syntax
sudo nginx -t
