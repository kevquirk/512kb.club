# Script to update sites.yml file for 512kb.club
#
# It updates requested number of entries in that file,
# starting with those having _earliest_ 'last_checked' date
# (those having non-date 'last_checked' field, like "N/A", are checked first).
import datetime
import os
import sys
import requests
import time

# create a file myauth.py with details of your gtmetrix account, like this:
# email='email@example.com'
# api_key='96bcab1060d838723701010387159086'
import myauth
# https://pypi.org/project/ruamel.yaml/
from ruamel.yaml import YAML

def summarizeHar(har):
    """Given a har file (parsed json object), returns total size of all responses, in bytes."""
    return sum((entry["response"]["content"]["size"] for entry in har["log"]["entries"]))

def request_URL_scan(URL_to_scan):
    cloudflare_scan_request_url = "https://api.cloudflare.com/client/v4/accounts/" + myauth.cloudflare_accountId + "/urlscanner/scan" # https://api.cloudflare.com/client/v4/accounts/{accountId}/urlscanner/scan
    payload = "{\"url\": \" " + URL_to_scan + " \"}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + myauth.cloudflare_API_TOKEN
    }
    response = requests.request("POST", cloudflare_scan_request_url, headers=headers, data=payload)
    response_JSON = response.json()
    if response_JSON["success"] == True: 
        if response_JSON["messages"][0]["message"] == "Submission successful": return response_JSON["result"]["uuid"]
        elif response_JSON["messages"][0]["message"] == "Submission unsuccessful: website was recently scanned": return response_JSON["result"]["tasks"][0]["uuid"]
        else: return "error"
    else: return "error"

def get_URL_scan_har(scan_uuid, retry_attempts=2):
    time.sleep(20)
    cloudflare_scan_har_url = "https://api.cloudflare.com/client/v4/accounts/" + myauth.cloudflare_accountId + "/urlscanner/scan/" + scan_uuid + "/har" #https://api.cloudflare.com/client/v4/accounts/{accountId}/urlscanner/scan/{scanId}/har
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + myauth.cloudflare_API_TOKEN
    }
    response = requests.request("GET", cloudflare_scan_har_url, headers=headers)
    response_JSON = response.json()
    if response_JSON["success"] == False: return "error"
    if len(response_JSON["result"]) > 0: return response_JSON["result"]["har"]
    if retry_attempts > 0: return get_URL_scan_har(scan_uuid, retry_attempts-1)
    return "error"

def countPageBytes(url):
    """Submits URL to Cloudflare URL Scanner, waits for analysis to complete, and returns dict of:
      {'kb': size in kilobytes rounded according to Cloudflare standard,
       'url': link to Cloudflare report (human-readable webpage)
      }"""
    scan_uuid = request_URL_scan(url)
    if scan_uuid == "error": return {'kb': 1000, 'url': 'error'}
    scan_har = get_URL_scan_har(scan_uuid)
    if scan_har == "error": return {'kb': 1000, 'url': 'error'}
    size = summarizeHar(scan_har)/1000 #Cloudflare uses 1000 vs GTMetrix which uses 1024
    if size<100:
        size = round(size,1)
    else:
        size = round(size)
    return {'kb': size, 'url': "https://radar.cloudflare.com/scan/" + scan_uuid + "/summary"}

def sizeToTeam(size):
    """Given a size in kilobytes, returns the 512kb.club team (green/orange/blue),
       or "N/A" if size is too big for 512kb.club"""
    if size<100:
        return "green"
    elif size<250:
        return "orange"
    elif size<=512:
        return "blue"
    else:
        return "N/A"

def append_line_to_md_table(md_filepath, data_to_append, newline=True):
    if not newline:
        with open(md_filepath, 'a') as f:
            f.write(data_to_append)
    else:
        with open(md_filepath, 'a') as f:
            f.write( "\n" + data_to_append)

def main():
    if len(sys.argv) != 3:
        print("Usage: %s /path/to/sites.yml number_of_oldest_sites_to_check" % sys.argv[0])
        exit(1)

    # load yaml
    yaml_sites_filepath = sys.argv[1]
    if not os.path.isfile(yaml_sites_filepath):
        print("Invalid filename: %s" % yaml_sites_filepath)
        exit(2)
    yaml=YAML()
    yaml.default_flow_style = False
    sites = yaml.load(open(yaml_sites_filepath,'r'))

    # number of sites left to check
    left = int(sys.argv[2])

    # table_of_updates_filepath = sys.argv[3]
    table_of_updates_filepath = os.path.dirname(os.path.realpath(__file__)) + "/updates.md"
    if os.path.isfile(table_of_updates_filepath): os.remove(table_of_updates_filepath)
    print("Site | old size (team) | new size (team) | delta (%) | Cloudflare | note")
    print("---- | --------------- | --------------- | --------- | ---------- | ----")
    append_line_to_md_table(table_of_updates_filepath, "Site | old size (team) | new size (team) | delta (%) | Cloudflare | note", False)
    append_line_to_md_table(table_of_updates_filepath, "---- | --------------- | --------------- | --------- | ---------- | ----")

    while left > 0:
        # find minimum (earliest) last_checked date
        # first, try entries where 'last_checked' is not a valid date (it can be "N/A")
        min_date = next((x['last_checked'] for x in sites if not isinstance(x['last_checked'],datetime.date)), None)
        if not min_date:
            # otherwise, find earliest of the found dates
            min_date = min((x['last_checked'] for x in sites if isinstance(x['last_checked'],datetime.date)))
        # TODO: abort if min_date is too close to present?
        # find first site with matching date
        site = next((x for x in sites if x['last_checked'] == min_date))
        # print first half of the row (with old data)
        oldsize = float(site['size'])
        oldteam = sizeToTeam(oldsize)
        print("[%s](%s) | %.1fkb (%s) | " % (site['domain'], site['url'], oldsize, oldteam), end='', flush=True)
        append_line_to_md_table(table_of_updates_filepath, "[%s](%s) | %.1fkb (%s) | " % (site['domain'], site['url'], oldsize, oldteam))
        # get new data
        result = countPageBytes(site['url'])
        if result['url'] == "error":
            left -= 1
            pass
        # analyze the result
        newsize = result['kb']
        newteam = sizeToTeam(newsize)
        delta = newsize-oldsize
        size_diff = round((newsize-oldsize)/oldsize*100)
        note = ''
        if abs(size_diff)>10:
            note = "big size change!"
        if oldteam != newteam:
            note = "team changed!!"
        if newsize>512:
            note = "too big for 512kb.club!!!"
        # print the second half of the row
        print(f"%.1fkb (%s) | %+.1fkb (%+d) | [report](%s) | %s" % (newsize, newteam, delta, size_diff, result['url'], note))
        # save the result
        site['size'] = newsize
        site['last_checked'] = datetime.date.today()
        yaml.dump(sites,open(yaml_sites_filepath,'w'))
        append_line_to_md_table(table_of_updates_filepath, "%.1fkb (%s) | %+.1fkb (%+d) | [report](%s) | %s" % (newsize, newteam, delta, size_diff, result['url'], note), False)
        left -= 1

if __name__ == '__main__':
    main()
