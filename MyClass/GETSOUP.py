import ssl, time
from bs4 import BeautifulSoup
from urllib import request

HEAD = dict({})
HEAD['USER-AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
CONTEXT = ssl._create_unverified_context()


def get_url_single(url, headers=None, decode='utf-8'):
    if headers is not None:
        HEAD.update(headers)
    req = request.Request(url, headers=HEAD)
    if "https" in url:
        response = request.urlopen(req, context=CONTEXT)
    else:
        response = request.urlopen(req)
    html = response.read().decode(decode)
    soup = BeautifulSoup(html, 'lxml')
    
    return soup


def get_url_list(url, headers=None, decode='utf-8'):
    if headers is not None:
        HEAD.update(headers)
    soup = list([])
    
    for each in url:
        req = request.Request(each, headers=HEAD)
        if "https" in url:
            response = request.urlopen(req, context=CONTEXT)
        else:
            response = request.urlopen(req)
        html = response.read().decode(decode)
        soup.append(BeautifulSoup(html, 'lxml'))
    
    return soup

