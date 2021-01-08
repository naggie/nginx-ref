#!/usr/bin/env python3
import os
import subprocess
# enumerates server_names to delete unused certificates

# ASSUMES ONE DOMAIN PER FILE

os.chdir("/etc/nginx/conf.d")

server_names = set()

# TODO factor this
for fp in os.listdir():
    with open(fp) as f:
        for line in f:
            if 'server_name' in line:
                domain = line.split()[1].strip(';')
                server_names.add()
                break

certificates = set(os.listdir("/etc/letsencrypt/live/"))
certificates.discard('README')

dangling = certificates - server_names

for name in dangling:
    subprocess.check_call(['certbot', 'delete', '-n', '--cert-name', name])
