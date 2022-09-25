import sys

import validators
from database import connect_db
from datetime import datetime
from getalive import httpx_parser
from naabu_parse import naabu_parser
from subdomain_parse import run_sub_parser


def subdomain_enum(target, domain, bbplatform):
    valid_domain = validators.domain(domain)
    if valid_domain:
        run_sub_parser(target, domain, bbplatform)
    else:
        raise NameError(
            sys.exit(
                f"{domain} is not a valid domain patterns, ex: example.com"
            )
        )


def list_subdomains(target):
    db = connect_db()
    collection = db["subdomains"]
    query = collection.find({"target": target})
    return query


def naabu_scan(target):
    naabu_parser(target)


def getalive(target):
    httpx_parser(target)


def list_urls_from_target(target):
    # TODO: verify if target is in database
    db = connect_db()
    collection = db["alivehosts"]
    query = collection.find({"target": target})

    return query


def save_subdomains(target, domain, file):
    db = connect_db()
    collection = db["subdomains"]
    all_subs = clean_file(file)
    for sub in all_subs:
        data = {
            "domain": domain,
            "subdomain": sub,
            "target": target,
            "date": datetime.now(),
        }

        if collection.find_one({"subdomain": sub}):
            print(f"Document already exists: {sub}")
        else:
            collection.insert_one(data)
            print(f"Inserted {sub}")
            

def clean_file(file):
    clean_subs = set()
    with open(file, "r") as file_:
        for line in file_:
            clean_subs.add(line.rstrip("\n"))

    return clean_subs
        