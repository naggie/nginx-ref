#!/usr/bin/env python3
import os
import subprocess
# enumerates domains to initialise certbot

os.chdir("/etc/nginx/conf.d")

domains = set()

for fp in os.listdir():
    with open(fp) as f:
        for line in f:
            if 'server_name' in line:
                domains.add(line.split()[1].strip(';'))

for domain in domains:
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
