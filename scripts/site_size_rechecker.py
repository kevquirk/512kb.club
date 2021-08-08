# Script to update sites.yml file for 512kb.club
#
# It updates requested number of entries in that file,
# starting with those having _earliest_ 'last_checked' date
# (those having non-date 'last_checked' field, like "N/A", are checked first).
import datetime
import os
import sys

# create a file myauth.py with details of your gtmetrix account, like this:
# email='email@example.com'
# api_key='96bcab1060d838723701010387159086'
import myauth
# https://github.com/aisayko/python-gtmetrix
from gtmetrix import *
# https://pypi.org/project/ruamel.yaml/
from ruamel.yaml import YAML

def summarizeHar(har):
    """Given a har file (parsed json object), returns total size of all responses, in bytes."""
    return sum((entry["response"]["content"]["size"] for entry in har["log"]["entries"]))

def countPageBytes(url):
    """Submits URL to gtmetrix, waits for analysis to complete, and returns dict of:
      {'kb': size in kilobytes rounded according to gtmetrix standard,
       'url': link to gtmetrix report (human-readable webpage)
      }"""
    # TODO: error checking in the following 4 lines
    my_test = gt.start_test(url)
    result = my_test.fetch_results(0)
    har = my_test._request(my_test.har)
    size = summarizeHar(har)/1024
    if size<100:
        size = round(size,1)
    else:
        size = round(size)
    return {'kb': size, 'url':result['results']['report_url']}

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

def main():
    if len(sys.argv) != 3:
        print("Usage: %s /path/to/sites.yml number_of_oldest_sites_to_check" % sys.argv[0])
        exit(1)

    # load yaml
    filename = sys.argv[1]
    if not os.path.isfile(filename):
        print("Invalid filename: %s" % filename)
        exit(2)
    yaml=YAML()
    yaml.default_flow_style = False
    sites = yaml.load(open(filename,'r'))

    global gt
    # workaround to allow "+" symbol in email
    # see also https://github.com/aisayko/python-gtmetrix/pull/18
    gt = GTmetrixInterface('a@b.cd','123')
    gt.auth=(myauth.email, myauth.api_key)

    # number of sites left to check
    left = int(sys.argv[2])
     
    print("Site | old size (team) | new size (team) | delta (%) | GTMetrix | note")
    print("---- | --------------- | --------------- | --------- | -------- | ----")

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
        # get new data
        result = countPageBytes(site['url'])
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
        print(f"%.1fkb (%s) | %+.1fkb (%+d) | [report](%s#waterfall) | %s" % (newsize, newteam, delta, size_diff, result['url'], note))
        # save the result
        site['size'] = newsize
        site['last_checked'] = datetime.date.today()
        yaml.dump(sites,open(filename,'w'))
        left -= 1

if __name__ == '__main__':
    main()
