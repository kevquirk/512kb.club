# 512KB Club

The internet has become a **bloated mess**. Massive JavaScript libraries, countless client-side queries and overly complex frontend frameworks are par for the course these days.

When online newspapers like [The Guardian](https://www.theguardian.com/uk) are **over 4MB in size**, you know there's a problem. Why does an online newspaper need to be over 4MB in size? It's crazy.

But we can make a difference - all it takes is some optimisation. Do you really need that extra piece of JavaScript? Does your WordPress site need a theme that adds lots of functionality you're never going to use? Are those huge custom fonts really needed? Are your images optimised for the web?

**The 512KB Club** is a collection of performance-focused web pages from across the Internet. To qualify your website must satisfy **both** of the following requirements:

1. It must be an actual site that contains a reasonable amount of information, not just a couple of links on a page ([more info here](https://512kb.club/#lightweight-notice)).
2. Your total UNCOMPRESSED web resources must not exceed 512KB.

## How to create a PR to add your site to the 512KB Club

1. Fork this repository.
2. Get the **UNCOMPRESSED** size of your website's homepage.
    1. Do a <a target="_blank" href="https://gtmetrix.com">GTMetrix scan</a> on your website.
    2. Once complete, click on the **Waterfall** tab to make sure the **uncompressed** size of your site is less than 512KB.
3. Navigate to [`_data/sites.yml`](./_data/sites.yml) and add your site (template below).
4.  **When creating the PR, please include a link to the GT Metrix results in the PR comment.**

### Site template

#### Sample
```
- domain: example.com
  url: http://example.com/ (Make sure you keep the trailing slash)
  size: 2.5
  last_checked: 2021-05-26 (YYYY-MM-DD)
```
#### Blank
```
- domain:
  url:
  size:
  last_checked:
```

**NOTE:** Entries are automatically sorted by domain name. Please add your site to the list without worrying about the alphabetical order. Our continuous integration process will handle the sorting for you. Just ensure that the details for your site are correctly formatted as per the existing entries.

## Automation of site size check

You can find [instructions](scripts/docs_site_size_rechecker.md) on how to get the GTmetrix size using a script in the [scripts](scripts/) folder
