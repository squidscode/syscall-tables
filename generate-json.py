import argparse
import json
from bs4 import BeautifulSoup as bs
from colored import Fore, Back, Style
import requests

COLORS = [
    Fore.red,
    Fore.yellow,
    Fore.green,
    Fore.cyan,
    Fore.blue,
]
URLS = {
    "x86-64": "https://x64.syscall.sh/",
    "arm": "https://arm.syscall.sh/",
    "arm64": "https://arm64.syscall.sh/",
    "x86": "https://x86.syscall.sh/",
}

def main(url: str, output_file: str):
    print(f"{Fore.cyan}Selected URL:{Style.reset} {url}")
    content = requests.get(url).content
    soup = bs(content, "html.parser")
    table = soup.find("table")
    thead = table.find("thead")
    tbody = table.find("tbody")
    headers = []
    for th in thead.find("tr"):
        if th.text.strip() == "":
            continue
        headers.append(th.text.strip())
    print(f"{Fore.cyan}Collected Headers:{Style.reset} {headers}")

    syscall_map = {}
    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")
        row = int(tds[0].text)
        syscall_map[row] = {}
        print(f"{Fore.cyan}Syscall #{row}:{Style.reset}")
        for col, th in enumerate(tds):
            # check that the NR column is properly formatted
            syscall_map[row][headers[col]] = th.text.strip()
            print(f"  {Fore.red}{headers[col]}{Style.reset} = \"{th.text.strip()}\"")

    with open(output_file, "+w") as f:
        f.write(json.dumps(syscall_map))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="JSON Generator",
        description="Generates a `.json` file which specifies\
                     how each syscall is called on the given\
                     architecture."
    )
    parser.add_argument("architecture", choices=URLS.keys())
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()
    main(URLS[args.architecture], args.output)
