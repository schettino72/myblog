<!--
.. title: generating HTML with javascript
.. slug: javascript-html-generation
.. date: 2013/01/29 20:00
.. tags: javascript, hoe.js
-->

I often hear people saying something like
"HTML must be created using a template engine, anything else is a bad practice".
I will try to demystify this *dogma*...

HTML
-----

HTML is a *text* document. But browsers don't handle the *text* directly.
It is first converted to DOM (document object model).
So HTML is more like a declarative way to describe a user interface program.

This is a very important distinction, one is **text** the other is an **object**
in a system.

Most components (HTML tags) simply describe how to display some data but other
are actual UI components.
For example a link (`a` tag) has an associated interaction with the user,
but being part of the standard the browser already knows how to handle it.
You don't need to write code for it, you just need to declare its `href`...


server-side templates
----------------------

At some point the web moved from static HTML pages to dynamically generated
HTML by the server side. After some time people realized that mixing *text*
generation in the code could get quite messy. So they started using template
engines.

A template engines combine a template with some data source to create a HTML *text* document.

Nowadays it is pretty much an established consensus that when generating HTML on
the servers-side you should use a template engine,
and I agree that's the right thing to do.


javascript templates
---------------------

As the web evolved the code started to move from server to client.
And the templates came together...

But wait. The server has no access to the DOM it can only create HTML *text*.
Javascript has direct access to the DOM!

Should we *always* programmatically write some *text* in a declarative interface
to create some UI components? Why not directly create these UI objects?


comparison
------------

Lets compare different ways to modify the DOM using javascript
to generate the content `<div>Hello there</div>`.

1) using DOM API

~~~~{.javascript}
var myDiv = document.createElement("div");
var myContent = document.createTextNode("Hello there!");
myDiv.appendChild(myContent);
document.body.appendChild(myDiv);
~~~~

Note this is not writing HTML *text* (although sometimes we may call it this way).
It is manipulating the DOM directly. Oh, yes, it sucks :)


2) using jQuery

~~~~{.javascript}
$('body').append($('<div>Hello there!</div>'));
~~~~

That's funny, even that we are manipulating the DOM directly you must write HTML markup.


3) another DOM API ([hoe.js](http://hoejs.schettino72.net/))

~~~~{.javascript}
$('body').append(div('Hello there!'));
~~~~

That looks more reasonable.


4) using templates ([Handlebars](http://handlebarsjs.com/))

~~~~{.javascript}
template = Handlebars.compile("<div>{{content}}</div>")
$('body').append(template({content: 'Hello there!'}));
~~~~

This example is too contrived, normally you would put the template
in a `script` tag.


declarative vs imperative
---------------------------

So which one is better? The answer is, of course, it depends...

Declarative is good for data. If you are just laying out the structure
for some data, and using some existing UI component (HTML-tag).
Using a template you will get a much more readable code.

example (handlebars):

~~~~{.HTML}
<ul class="people_list">
  {{#each people}}
  <li>{{this}}</li>
  {{/each}}
</ul>
~~~~


Declarative is also good if you are just using some custom component.
In the example bellow a framework/library would look for elements
with a `class` attribute indicating the widget to be used and
the `data-` attributes to configure it.

~~~~{.HTML}
<ul class="widget-XYZ" data-opt-a="5">
   some content
</ul>
~~~~


Template has a big disadvantage, it produces *text* and
loses the direct access to the DOM
that is available from javascript.

When the web "moved" from server to the client the default UI
elements provided by HTML were not enough to provide a rich user experience.
So developers often need to create new UI components in javascript.

If you are **creating** a new UI component where
you need to specify the behavior for a click and other actions you must
manipulate the object in the DOM because you need to attach events.

example (hoe.js):

~~~~{.javascript}
var myComponent = div('click me');
myComponent.click(function(){alert('Hello there!')});
~~~~

So in one way or another you will have to get back a reference to the created
object. If you use a template this is usually done by a CSS selector.

Using a CSS selector is bad for many reasons. It might be slow (need to search
in the DOM). The code is error prone because it depends on attribute values
that are far away from the code. The selectors have two meanings
(styling with CSS and reference in javascript) that can gets confusing.

Another choice would be that your template/HTML reference the javascript code.
For very simple things this was always possible using `onclick` and other
attributes for events. Some frameworks provide more sophisticated mechanism like
associating with a "controller", etc.
The problem with this approach is that it doesn't scale as your component evolves.
When it gets more complex you try to stuff more logic in the template.
When your template can't handle it anymore you need to *throw away* your template
and re-write it in javascript...


conclusion
-------------

If you are **creating** an UI component, manipulating the DOM from javascript
is probably your best option.

If you are just filling some data and **using** existing components, templates
are probably better for you.


