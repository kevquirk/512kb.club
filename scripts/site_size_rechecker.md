`site_size_rechecker.py` is a script to recheck and update sizes of sites
=========================================================================

It reads sites.yml file,
and updates requested number of entries in that file -
starting with those having _earliest_ `last_checked` date
(those having non-date `last_checked` field, like "N/A", are checked first).

Requirements
------------

* Python 3
* a [gtmetrix.com](https://gtmetrix.com/) account

Installation
------------

1. register at [gtmetrix.com](https://gtmetrix.com/)
2. open [account](https://gtmetrix.com/dashboard/account) section
3. In the Your Plan - API Usage, generate API key.
    Also note that upon registration, you're given 100 credits "for testing", and every day at noon Vancouver time your credits are refilled _up to_ 10 (so only if you have less than 10). We need only the most basic kind of report, which costs 0.7 credits, hence after test cregits are all used up one account can request 10/0.7=14 reports per day.
4. Install "ruamel.yaml" Python library (available via [pip][yml-pip] or a [package manager][yml-arch]).
5. install [python-gtmetrix][repo].
    While they have a pip project, there is a [comment](https://github.com/aisayko/python-gtmetrix/issues/13#issuecomment-781785672) suggesting to install from git. In my case, I just cloned their [repo][] and put this script into its root (next to setup.py). From all their requirements.txt file they seem to need only [requests][req] which have [pip][req-pip] and an [OS package][req-os].
6. next to your script, create myauth.py file with a content like this:
    ````
    email='email@example.com'
    api_key='96bcab1060d838723701010387159086'
    ````
    with email which you used to register at gtmetrix.com (step 1) and api key which you got on step 3

[repo]: https://github.com/aisayko/python-gtmetrix

[req]: http://python-requests.org/
[req-pip]: https://pypi.org/project/requests/
[req-os]: https://archlinux.org/packages/extra/any/python-requests/
[yml-pip]: https://pypi.org/project/ruamel.yaml/
[yml-arch]: https://archlinux.org/packages/community/any/python-ruamel-yaml/

Usage
-----

Run this script like this:

    python script2.py ../512kb.club/_data/sites.yml 1

where 1 is the number of websites to be updated (starting with oldest ones)

If everything goes right, you should get a table-like output which you can just paste into Guthub PR:

    Site | old size (team) | new size (team) | delta (%) | GTMetrix | note
    ---- | --------------- | --------------- | --------- | -------- | ----
    [docs.j7k6.org](https://docs.j7k6.org/) | 73.0kb (green) | 72.9kb (green) | -0.1kb (-0%) | [report](https://gtmetrix.com/reports/docs.j7k6.org/PkIra4ns/#waterfall) | 

Note that it "hangs" for about 30 seconds in the middle of each line except first two,
because first it prints site name and old size,
then waits for gtmetrix scan to finish,
and after that prints new size and rest of the line.

This is done so if script encounters an issue when running gtmetrix scan,
you know which site it happened with,
and can either check it manually or ask the script to exclude this site from checking.

Fine-tuning
-----------

To decrease waiting time,
edit the [gtmetrix/interface.py][int] file in python-gtmetrix repo,
and change the number `30` in line 85 to something smaller - for example, change this line from

	time.sleep(30)

to

	time.sleep(3)

This will decrease the delay between each check when the script is waiting for gtmetrix scan to finish.

The [recommended poll interval][rec] is 1 second.
I suggest setting it to 3 seconds.
By default in interface.py file it's set to 30 seconds.

[int]: https://github.com/aisayko/python-gtmetrix/blob/master/gtmetrix/interface.py#L85
[rec]: https://gtmetrix.com/api/docs/0.1/#api-test-state

Troubleshooting
---------------

In case you encounter an issue when using this script,
you can ask @Lex-2008 for help
(don't hesitate to provide as much information as possible:
all output that this script produces and in what state your `sites.yml` is.
Is it same as on master? Is it modified in some way?).

To exclude a site from checking, update its `last_checked` date
(set it to today or at least something different from oldest one).

To debug why the script "hangs" when checking some site,
edit the [gtmetrix/interface.py][int2] file in python-gtmetrix repo,
and add new line after line 86 - change this:

	response_data = self._request(self.poll_state_url)
	self.state = response_data['state']

to this:

	response_data = self._request(self.poll_state_url)
	print(response_data)
	self.state = response_data['state']

This will break nicely formatted table output,
but you will see raw response from gtmetrix API.
In my case, I had a site for which gtmetrix API responses looked like this:

	{'resources': {}, 'error': 'An error occurred fetching the page: HTTPS error: hostname verification failed', 'results': {}, 'state': 'error'}

and didn't change, but the script was waiting for 'state' to become 'completed', which obviously was not going to happen.

[int2]: https://github.com/aisayko/python-gtmetrix/blob/master/gtmetrix/interface.py#L86

Future plans
------------

Currently this script doesn't check any errors returned by gtmetrix.com API. That's next item on my list. Moreover, I will get rid of python-gtmetrix dependency, since it adds more troubles than benefits.

