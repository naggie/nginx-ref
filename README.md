For Ubuntu server 20.04+

Provides a reference implementation with:

* Let's encrypt automatic HTTPS
* Templates for proxy, authelia?, static files, etc
* A+ ssllabs rating
* Minimal but pretty self-contained error pages


The installer re-implements `/etc/nginx/`, deleting files as necessary. You
have been warned!


# How to

1. Run `./install.sh`
2. Add config files based on `examples/*` to `/etc/conf.d/`. One `server_name`
   per file. Convention: `/etc/nginx/conf.d/<domain>.conf`, not required.
3. Run `./initialise-certbot.py` to start automatic HTTP for all `server_name`s
   in `/etc/nginx/conf.d/`.

Note this implementation uses Certbot's `certonly` option, so the
certificate/key path must be hardcoded into the config files as in the
examples. See `./initialise-certbot.py` for more information.


# Error pages

`epgen/` contains a script to generate the error pages in `error-pages/`. It can also
embed a logo.
