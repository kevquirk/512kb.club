# Site Size Rechecker Script Documentation

> **🚨 IMPORTANT 🚨**: This document is out of date, as we're no longer using GTMetrix. We since migrated to Cloudflare. More information can be found [here](https://github.com/kevquirk/512kb.club/issues/1366).

## Purpose
The main purpose of `site_size_rechecker.py` script is to automate the checking of older sites that are listed in the 512kb.club and ensuring that the size is updated.

## How it works
1. Read `sites.yml` file
1. Analyze `last_checked` key pair
    1. Sort key pair in ascending order _earliest first_
    1. Non-date values are listed before dated values such as **"N/A"**

## Requirements

* [GTmetrix.com](https://GTmetrix.com/) account
* Python3 with pip
* ruamel.yaml

## Installation

1. Create an account with [GTmetrix.com](https://gtmetrix.com/)
    1. Go to [account settings](https://gtmetrix.com/dashboard/account) and generate an API Key
1. Install **ruamel.yaml** Python library (available via [pip](https://pypi.org/project/ruamel.yaml/) or a [package manager](https://archlinux.org/packages/community/any/python-ruamel-yaml/)).
1. Install [python-gtmetrix](https://github.com/aisayko/python-gtmetrix).
    1. It is [recommened](https://github.com/aisayko/python-gtmetrix/issues/13#issuecomment-781785672) to just Git clone the repo as they only require [requests](http://python-requests.org/) which have [pip](https://pypi.org/project/requests/) and an [OS package](https://archlinux.org/packages/extra/any/python-requests/).
1. Create authintication file named `myauth.py` with the following format:
    ```py
    email='email@example.com'
    api_key='96bcab1060d838723701010387159086'
    ```
    1. email: is the one used in creating a GTmetrix account
    1. api_key: is what was generated in step 1.1
1. Copy the `site_size_rechecker.py` and `myauth.py` into the `python-gtmetrix` cloned in step 3

_Note:_  Under the new plan you will first receive 100 credits from GTmetrix for testing. after which you will get a refill of 10 credits every day at `8:45 PM +0000`. This script uses 0.7 credits for each site check. which is about 14 site reports per day per person
## Usage

while in the `python-gtmetrix` folder run:

```sh
python script2.py ../512kb.club/_data/sites.yml XY
```
_Note:_ XY stands for the number of sites to be checked

### Successful Output

Successful output will generate a table in markdown file which _**Must**_ be put in the PR such as [#450](https://github.com/kevquirk/512kb.club/pull/450)
```md
Site | old size (team) | new size (team) | delta (%) | GTmetrix | note
---- | --------------- | --------------- | --------- | -------- | ----
[docs.j7k6.org](https://docs.j7k6.org/) | 73.0kb (green) | 72.9kb (green) | -0.1kb (-0%) | [report](https://GTmetrix.com/reports/docs.j7k6.org/PkIra4ns/#waterfall) |
```
_Note:_ In the middle of each line it takes about 30 seconds in wait-time to output the rest of the line. This is due to the time it takes to finish the GTmetrix scan

This can be beneficial to know if a site has a problem that can be used to check the site or remove it from the checking.


If everything goes right, you should get a table-like output which you can just paste into Github PR:

Note that it "hangs" for about 30 seconds in the middle of each line except the first two,
as it first prints site name and old size,
then waits for GTmetrix scan to finish,
and after that prints new size and rest of the line.

This is done so if the script encounters an issue when running GTmetrix scan,
you know which site it happened with,
and can either check it manually or exclude the site from checking.

## Fine-tuning

### Wait-time

To decrease waiting time,
edit the [python-gtmetrix/gtmetrix/interface.py](https://github.com/aisayko/python-gtmetrix/blob/master/gtmetrix/interface.py#L85) file and change the number `30` in line 85 to a smaller number - for example, change this line from
```py
time.sleep(30)
```
to
```py
time.sleep(3)
```
This will decrease the delay between each check when the script is waiting for the GTmetrix scan to finish.

The [recommended poll interval](https://GTmetrix.com/api/docs/0.1/#api-test-state) is 1 second.
I suggest setting it to 3 seconds.
By default in interface.py file is set to 30 seconds.

### Excluding site from checks

To exclude a site from checks you can either remove the site or change the `last_checked` Key-Pair to today's date or a date in the future to make it last in the list.

## Troubleshooting

In case you encounter an issue with this script open a [New Issue](https://github.com/kevquirk/512kb.club/issues) and tagging @Lex-2008

Please provide as much information as possible such as:
* All Output
* Current state of `sites.yml` if it's from the `master` branch, or has been modified

To debug why the script "hangs" when checking some site, edit the [ python-gtmetrix/gtmetrix/interface.py](https://github.com/aisayko/python-GTmetrix/blob/master/GTmetrix/interface.py#L86) file
and a new 87th line which would looke like this:

Orginal file
```py
response_data = self._request(self.poll_state_url)
self.state = response_data['state']
```
Edited file
```py
response_data = self._request(self.poll_state_url)
print(response_data)
self.state = response_data['state']
```
This will break the nicely formatted table output, but you will see the raw response from GTmetrix API.
```sh
{'resources': {}, 'error': 'An error occurred fetching the page: HTTPS error: hostname verification failed', 'results': {}, 'state': 'error'}
```

## Future plans

Currently, this script doesn't check any errors returned by GTmetrix.com API. That's the next item on my list. Moreover, I will get rid of python-GTmetrix dependency, since it adds more troubles than benefits.
