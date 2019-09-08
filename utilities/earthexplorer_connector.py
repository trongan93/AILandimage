import sys
import re
import urllib
import urllib.request
import urllib.response
import urllib.parse
import urllib.error

# "Connection to Earth explorer with proxy

def connect_earthexplorer_proxy(proxy_info, usgs):
    print("Establishing connection to Earthexplorer with proxy...")
    # contruction d'un "opener" qui utilise une connexion proxy avec autorisation
    cookies = urllib.request.HTTPCookieProcessor()
    proxy_support = urllib.request.ProxyHandler({"http": "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info,
                                          "https": "http://%(user)s:%(pass)s@%(host)s:%(port)s" % proxy_info})
    opener = urllib.request.build_opener(proxy_support, cookies)

    # installation
    urllib.request.install_opener(opener)
    # deal with csrftoken required by USGS as of 7-20-2016
    data = urllib.request.urlopen("https://ers.cr.usgs.gov").read()
    m = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', data)
    if m:
        token = m.group(1)
    else:
        print("Error : CSRF_Token not found")
        sys.exit(-3)
    # parametres de connection
    params = urllib.parse.urlencode(
        dict(username=usgs['account'], password=usgs['passwd'], csrf_token=token))
    # utilisation

    request = urllib.request.Request("https://ers.cr.usgs.gov", params, headers={})
    f = urllib.request.urlopen(request)
    data = f.read()
    f.close()

    if data.find('You must sign in as a registered user to download data or place orders for USGS EROS products') > 0:
        print("Authentification failed")
        sys.exit(-1)
    return

# "Connection to Earth explorer without proxy

def connect_earthexplorer_no_proxy(usgs):
    # mkmitchel (https://github.com/mkmitchell) solved the token issue
    cookies = urllib.request.HTTPCookieProcessor()
    opener = urllib.request.build_opener(cookies)
    urllib.request.install_opener(opener)

    data = urllib.request.urlopen("https://ers.cr.usgs.gov").read()
    data = data.decode('utf-8')
    m = re.search(r'<input .*?name="csrf_token".*?value="(.*?)"', data)
    if m:
        token = m.group(1)
    else:
        print("Error : CSRF_Token not found")
        sys.exit(-3)

    params = urllib.parse.urlencode(
        dict(username=usgs['account'], password=usgs['passwd'], csrf_token=token))
    params = params.encode('utf-8')
    request = urllib.request.Request(
        "https://ers.cr.usgs.gov/login", params, headers={})
    f = urllib.request.urlopen(request)

    data = f.read()
    f.close()
    data = data.decode('utf-8')
    if data.find('Authentication Failed') > 0:
    # if data.find('You must sign in as a registered user to download data or place orders for USGS EROS products') > 0:
        print("Authentification failed")
        sys.exit(-1)
    return

