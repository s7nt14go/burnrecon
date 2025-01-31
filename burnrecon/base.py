import sys

import validators
from database import connect_db
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
