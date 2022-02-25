---
permalink: /
layout: default
hasRandomBtn: true
---
The internet has become a <b>bloated mess</b>. Massive JavaScript libraries, countless client-side queries and overly complex frontend frameworks are par for the course these days.

When popular website like [The New York Times](https://www.nytimes.com/) are **[over 15MB in size](https://gtmetrix.com/reports/www.nytimes.com/Dz1IEZl0/)** (nearly 50% of which is JavaScript!), you know there's a problem. Why does any site need to be that huge? It's crazy.

But we can make a difference - all it takes is some optimisation. Do you really need that extra piece of JavaScript? Does your WordPress site need a theme that adds lots of functionality you're never going to use? Are those huge custom fonts really needed? Are your images optimised for the web?

**The 512KB Club** is a collection of performance-focused web pages from across the Internet. To qualify your website must satisfy **both** of the following requirements:

1. It must be an actual site that contains a reasonable amount of information, not just a couple of links on a page ([more info here](/faq/#lightweight-notice)).
2. Your total UNCOMPRESSED web resources must not exceed 512KB.

<br>
<div class="centre">
  <a class="button" href="/faq">View FAQ for more details</a>
</div>

<br>
<hr>

<br>
<div class="divrandom centre">
  <a class="button random" href="#100" onclick="randomSite(); return false;">Visit a Random Site</a>
</div>

{:.jump}
* **Jump to:**
* [Green Team (&lt;100KB)](#100)
* [Orange Team (&lt;250KB)](#250)
* [Blue Team (&lt;512KB)](#512)

<h2 id="100">The Green Team (&lt;100KB) <span class="small"><a href="#top">^ Top ^</a></span></h2>
<ul class="green">
    {%- assign site_domains = site.data.sites | sort: 'size' -%}
    {%- for item in site_domains -%}
        {%- if item.size >= 0 and item.size <= 100 -%}
            {% include teams.html %}
        {%- endif -%}
    {%- endfor -%}
</ul>

<h2 id="250">The Orange Team (&lt;250KB) <span class="small"><a href="#top">^ Top ^</a></span></h2>
<ul class="orange">
    {%- assign site_domains = site.data.sites | sort: 'size' -%}
    {%- for item in site_domains -%}
        {%- if item.size > 100 and item.size <= 250 -%}
            {% include teams.html %}
        {%- endif -%}
    {%- endfor -%}
</ul>

<h2 id="512">The Blue Team (&lt;512KB) <span class="small"><a href="#top">^ Top ^</a></span></h2>
<ul class="blue">
    {%- assign site_domains = site.data.sites | sort: 'size' -%}
    {%- for item in site_domains -%}
        {%- if item.size > 250 and item.size <= 512 -%}
            {% include teams.html %}
        {%- endif -%}
    {%- endfor -%}
</ul>
