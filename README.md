# 512KB Club

The internet has become a **bloated mess**. Massive JavaScript libraries, countless client-side queries and overly complex frontend frameworks are par for the course these days.

When online newspapers like [The Guardian](https://www.theguardian.com/uk) are **over 4MB in size**, you know there's a problem. Why does an online newspaper need to be over 4MB in size? It's crazy.

But we can make a difference - all it takes is some optimisation. Do you really need that extra piece of JavaScript? Does your WordPress site need a theme that adds lots of functionality you're never going to use? Are those huge custom fonts really needed? Are your images optimised for the web?

**The 512KB Club** is a collection of performance-focused web pages from across the Internet. To qualify your website must satisfy **both** of the following requirements:

1. It must be an actual site that contains a reasonable amount of information, not just a couple of links on a page ([more info here](https://512kb.club/#lightweight-notice)).
2. Your total UNCOMPRESSED web resources must not exceed 512KB.

## How to create a PR to add your site to the 512KB Club

1. Fork this repository.
2. Get the **UNCOMPRESSED** size of your website's homepage and work out which team it should be in.
    a. Less than 100KB - **Green Team**
    b. Less than 250KB - **Orange Team**
    c. Less than 512KB - **Blue Team**
3. Once you know which team you're in, navigate to `_data/<colour>-team.yml`
4. Add your site to the list using the template below:

```
- domain: example.com
  url: https://example.com
  size: 75.2
```

**NOTE:** You site needs to be added to the list in **size order**, so please make sure your site is in the correct place within the list, or your PR will be rejected. If you site is the same size as someone else's in the list, please add yours before or after alphabetically.
