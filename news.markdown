---
layout: post
title: News
permalink: /news/
---
## The latest news about COBALT

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ post.url }}"><span style="font-size:large">{{ post.title }}</span></a> (Posted on {{ post.date | date_to_long_string: "ordinal" }})
      {{ post.excerpt }}
    </li>
  {% endfor %}
</ul>
