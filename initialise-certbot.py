#!/usr/bin/env python3
import os
import subprocess
# enumerates domains to initialise certbot

os.chdir("/etc/nginx/conf.d")

domains = dict()

LETSENCRYPT_CERT_PATH = "/etc/letsencrypt/live/%s/fullchain.pem"

def get_letsencrypt_domains(content):
    # get server name
    for line in content.splitlines():
        line = line.strip()
        if line.startswith('server_name'):
            domain = line.split()[1].strip(';')

            # check certbot is used for this domain
            if LETSENCRYPT_CERT_PATH % domain in content:
                yield domain


# find all domains, map to conf file
for fp in os.listdir():
    if not fp.endswith(".conf"):
        continue

    with open(fp) as f:
        for domain in get_letsencrypt_domains(f.read()):
            domains[domain] = fp

# remove domains that are already configured. Note there could be multiple per
# file
for domain, conffile in domains.copy().items():
    keyfile = LETSENCRYPT_CERT_PATH % domain

    if os.path.exists(keyfile):
        print("\033[33m%s\033[0m" % "\nSkipping existing %s..." % domain)
        del domains[domain]
        continue

for domain, conffile in domains.items():
    keyfile = LETSENCRYPT_CERT_PATH % domain

    # we use certonly to manage our own files instead of allowing certbot to
    # edit them (so version control is easier)
    # As such, before a certificate is obtained for the first time, a reference
    # to a non-existent certificate will be in the requisite configuration
    # file. As the certbot-nginx plugin needs to reload nginx, this will fail
    # unless the config file is disabled temporarily.
    # This prevents a chicken-and-egg situation; isolate all uninitialised configs.
    for fp in domains.values():
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
    for fp in domains.values():
        os.rename(fp + '.disabled', fp)

# reload nginx, even though certbot would have done it -- it's necessary due to
# the temporary config disabling we did.
subprocess.check_call(['systemctl', 'reload', 'nginx'])
