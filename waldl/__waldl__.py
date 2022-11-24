import httpx

import platform
import os
import sys
import time
import json
import re
from os.path import expanduser
import subprocess

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0"
}

client = httpx.Client(headers=headers, follow_redirects=True, timeout=None)

def determine_path() -> str:

    plt = platform.system()

    if plt == "Linux" or plt == "Darwin":
        return expanduser("~/Downloads")
    else:
        print("[!] Unsupported OS")

walldir: str = determine_path()

home = expanduser("~")
cachedir = f"{home}/.cache/wallhaven"

sorting = "random"
atleast = "1920x1080"
ratios = "16x9"
seed = r"[a-zA-Z0-9]{6}"

apikey = "xkTtX4xkWoXATYW1v1GF4fQfy3FWhnoR"
quality = "large"


if len(sys.argv) == 1:
    query = input("Search: ")
    if query == "":
        print("ValueError: no query parameter provided")
        exit(0)
else:
    query = " ".join(sys.argv[1:])

query = query.replace(" ", "+")

#os.remove(f"{cachedir}/urls.txt")
#os.rmdir(f"{cachedir}")

os.mkdir(f"{home}/.cache/wallhaven")
os.system(f"touch {home}/.cache/wallhaven/urls.txt")

datafile = r"/tmp/wald.json"

def clean_up():
    print("Cleaning up...")
    os.remove(f"{cachedir}/urls.txt")
    os.rmdir(f"{cachedir}")
    os.remove(datafile)

def get_results(e):
    for page_no in range(0,2):
        get_results.j = client.get(f"https://wallhaven.cc/api/v1/search?api={apikey}",
                params={
                    "q": e,
                    "sorting": sorting,
                    "atleast": atleast,
                    "ratios": ratios,
                    "page": 1,
                    "seed": seed
                },
            ).text

        with open(datafile, "w") as file:
            file.write(get_results.j)

        time.sleep(0.001)

print("getting data...")
get_results(query)

with open(datafile, "r") as read_file:
    thumbnails = json.load(read_file)

#print(thumbnails["data"])

urls = re.findall(r'https:\/\/w.wallhaven.cc\/full\/[0-9]{2}\/wallhaven-[a-zA-Z0-9]{6}.[a-zA-Z]{3}', str(thumbnails["data"]))

for url in urls:
    with open(f"{cachedir}/urls.txt", "a") as file:
        file.write(f"{url}\n")

with open(f"{cachedir}/urls.txt", "r") as file:
    hehe = file.readlines()
    #count = 0
    for line in hehe:
        #count += 1
        args = [
            "aria2c",
            f"--dir={walldir}",
            "{}".format(line.strip())
        ]
        aria2_process = subprocess.Popen(args)
        aria2_process.wait()

try:
    subprocess.call(f"nsxiv -tfpo {walldir}", shell=True)
except Exception as e:
    subprocess.call(f"qview {walldir}/*", shell=True)

clean_up()
