from bs4 import BeautifulSoup
import sys
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import Timeout, SSLError, InvalidSchema
from urllib3.exceptions import InsecureRequestWarning, MaxRetryError, ConnectTimeoutError
import urllib3
import socket
from urllib3.connection import HTTPConnection

# Basic link crawler to check header status of sites referenced in xml files. Call with python3 linkCrawler.py.

infile = open("../devilfish_full.xml", "r")
contents = infile.read()
# print(contents)
soup = BeautifulSoup(contents, features="xml")
links = soup.find_all("ptr")
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.6) Gecko/20070802 SeaMonkey/1.1.4'
}

HTTPConnection.default_socket_options = (
    HTTPConnection.default_socket_options + [
        (socket.SOL_SOCKET, socket.SO_SNDBUF, 1000000),
        (socket.SOL_SOCKET, socket.SO_RCVBUF, 1000000)
    ]
)
sesh = requests.Session()
retries = Retry(total=5, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retries)
sesh.mount('http://', adapter)

errors = []

try:
    for link in links:
        urllib3.disable_warnings(category=InsecureRequestWarning)
        cleanLinks = (link.get('target'))
        x = sesh.get(cleanLinks, verify=False,
                     headers=headers, timeout=100)
        urllib3.PoolManager(cert_reqs='CERT_NONE')
        print(cleanLinks, "\n", x, x.reason, "\n")

except InsecureRequestWarning as a:
    errors.append(a)
    # pass
except ConnectionError as b:
    errors.append(b)
    # pass
except InvalidSchema as c:
    errors.append(c)
    # pass
except SSLError as d:
    errors.append(d)
    # pass
except Timeout as e:
    if (retries.total >= 5):
        errors.append(e)
        # pass
except ConnectTimeoutError as f:
    errors.append(f)
    # pass
except MaxRetryError as g:
    errors.append(g)
    # pass
except KeyboardInterrupt:
    sys.exit()

for error in errors:
    print(errors)
