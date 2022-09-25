#!/usr/bin/env python3
import sys, argparse, requests, json

BASE_URL = "https://crt.sh/?q={}&output=json"
subdomains = set()
wildcardsubdomains = set()

def crtsh(domain):
    try:
        response = requests.get(BASE_URL.format(domain), timeout=25)
        if response.ok:
            content = response.content.decode('UTF-8')
            jsondata = json.loads(content)
            for i in range(len(jsondata)):
                name_value = jsondata[i]['name_value']
                if name_value.find('\n'):
                    subname_value = name_value.split('\n')
                    for subname_value in subname_value:
                        if subname_value.find('*'):
                            if subname_value not in subdomains:
                                subdomains.add(subname_value)

    except:
        pass

    return subdomains