import os
import tempfile
from config import settings
from crtsh import crtsh
from datetime import datetime
from pathlib import Path
from database import connect_db

chaos_key = settings.CHAOS_TOKEN
security_trails_key = settings.SECURITY_TRAILS_TOKEN
github_key = settings.GITHUB_TOKEN

random_name = tempfile.NamedTemporaryFile(delete=False)
final_file = Path(random_name.name)


def exec_subfinder(domain):
    subfinder_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
    subfinder_cmd = f"subfinder -d {domain} -silent -o {subfinder_out}"
    os.system(subfinder_cmd)
    os.system(f"cat {subfinder_out} >> {final_file}")
    subfinder_out.unlink()


def exec_amass(domain):
    amass_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
    amass_cmd = f"amass enum -passive -d {domain} -o {amass_out}"
    os.system(amass_cmd)
    os.system(f"cat {amass_out} >> {final_file}")
    amass_out.unlink()


def exec_assetfinder(domain):
    assetfinder_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
    assetfinder_cmd = f"assetfinder -subs-only {domain} > {assetfinder_out}"
    os.system(assetfinder_cmd)
    os.system(f"cat {assetfinder_out} >> {final_file}")
    assetfinder_out.unlink()


def exec_chaos(domain):
    if chaos_key != '':
        chaos_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
        chaos_cmd = f"chaos -d {domain} -silent -key {chaos_key} -o {chaos_out}"
        os.system(chaos_cmd)
        os.system(f"cat {chaos_out} >> {final_file}")
        chaos_out.unlink()
    else:
        print('There is no chaos key defined. Chaos search will be skipped.')


def exec_crtsh(domain):
    crtsh_out = crtsh(domain)
    for subdomain in crtsh_out:
        os.system(f"echo {subdomain} >> {final_file}")


def exec_haktrails(domain):
    if security_trails_key != '':
        os.system(f"""echo "securitytrails:\n  key: {security_trails_key}" > ~/.config/haktools/haktrails-config.yml""")
        haktrails_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
        haktrails_cmd = f"echo {domain} | haktrails subdomains > {haktrails_out}"
        os.system(haktrails_cmd)
        os.system(f"cat {haktrails_out} >> {final_file}")
        haktrails_out.unlink()
    else:
        print('There is no Security Trails key defined. Security Trails search will be skipped.')


def exec_github_search(domain):
    if github_key != '':
        github_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
        github_cmd = f"~/tools/github-search/github-subdomains.py -d {domain} -t {github_key} > {github_out}"
        os.system(github_cmd)
        os.system(f"cat {github_out} >> {final_file}")
        github_out.unlink()
    else:
        print('There is no Security Trails key defined. Security Trails search will be skipped.')


def exec_findomain(domain):
    findomain_out = Path(tempfile.NamedTemporaryFile(delete=False).name)
    findomain_cmd = f"findomain -t {domain} -q -u {findomain_out}"
    os.system(findomain_cmd)
    os.system(f"cat {findomain_out} >> {final_file}")
    findomain_out.unlink()

def clean_results(domain):
    clean_subs = set()
    exec_subfinder(domain)
    exec_amass(domain)
    exec_assetfinder(domain)
    exec_chaos(domain)
    exec_haktrails(domain)
    exec_github_search(domain)
    exec_crtsh(domain)
    exec_findomain(domain)
    with open(final_file, "r") as file_:
        for line in file_:
            if line != '\n':
                clean_subs.add(line.rstrip("\n"))

    return clean_subs


def run_sub_parser(target, domain, bbplatform=""):
    # TODO: config to accept a list with domains
    db = connect_db()
    collection = db["subdomains"]
    all_subs = clean_results(domain)
    for sub in all_subs:
        data = {
            "domain": domain,
            "bbplatform": bbplatform,
            "subdomain": sub,
            "target": target,
            "date": datetime.now(),
        }

        if collection.find_one({"subdomain": sub}):
            print("Document already exists")
        else:
            collection.insert_one(data)
            print(f"Inserted {sub}")

    final_file.unlink()
