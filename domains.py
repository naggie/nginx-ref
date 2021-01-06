#!/usr/bin/env python3
import os

os.chdir("examples")

domains = set()

for fp in os.listdir():
    with open(fp) as f:
        for line in f:
            if 'server_name' in line:
                domains.add(line.split()[1].strip(';'))

print(domains)
