#!/usr/bin/env python3
import os
import subprocess
# enumerates domains to initialise certbot

# ASSUMES ONE DOMAIN PER FILE

os.chdir("/etc/nginx/conf.d")

domains = dict()

# TODO factor this
for fp in os.listdir():
    with open(fp) as f:
        for line in f:
            if 'server_name' in line:
                domain = line.split()[1].strip(';')
                domains[domain] = fp
                break

for domain, fp in domains.items():
    key = '/etc/letsencrypt/live/%s/fullchain.pem' % domain

    if os.path.exists(key):
        print("\033[33m%s\033[0m" % "\nSkipping existing %s..." % domain)
        continue

    # we use certonly to manage our own files instead of allowing certbot to
    # edit them (so version control is easier)
    # As such, before a certificate is obtained for the first time, a reference
    # to a non-existent certificate will be in the requisite configuration
    # file. As the certbot-nginx plugin needs to reload nginx, this will fail
    # unless the config file is disabled temporarily.
    # This prevents a chicken-and-egg situation.
    os.rename(fp, fp + '.disabled')

    print("\033[32m%s\033[0m" % "\nInitialising %s..." % domain)
    subprocess.check_call([
        "certbot",
        "certonly",
        "-n",
        "--agree-tos",
        "--register-unsafely-without-email",
        "--nginx",
        "--domain", domain,
    ])

    # re-enable
    os.rename(fp + '.disabled', fp)

# reload nginx, even though certbot would have done it -- it's necessary due to
# the temporary config disabling we did.
subprocess.check_call(['systemctl', 'reload', 'nginx'])
