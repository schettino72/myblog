<!--
.. title: mongodb setup for deployd on heroku
.. slug: mongodb-setup-deployd-heroku
.. date: 2013/01/27 00:00
.. tags: node.js, mongodb
-->

I am using [deployd](http://deployd.com/) to prototype an applicaton.
It's been great, really helped me focus on what matters for the prototype.

Today I reached the first milestone and decided to deploy it in
[heroku](http://www.heroku.com/).

I had a small problem because *deployd* uses an object to config *mongodb*,
but *heroku* provides only a URL to mongodb server...
So here is the script I am using to run *deployd* on *heroku*:

~~~~{.javascript}
var deployd = require('deployd');

// on heroku must use port from env
var port = process.env.PORT || 3000;

var url = require('url');
var db_url = url.parse(
    process.env.MONGOHQ_URL || "mongodb://:@localhost:27017/my_db_name");

var options = {
    port: port,
    db: {
        "host": db_url.hostname,
        "port": parseInt(db_url.port),
        "name": db_url.pathname.slice(1),
        "credentials": {
            "username": db_url.auth.split(':')[0],
            "password": db_url.auth.split(':')[1]
        }
    }
};

var server = deployd(options);
server.listen();

server.on('listening', function() {
  console.log("Server is listening on " + port);
});

server.on('error', function(err) {
  console.error(err);
  process.nextTick(function() { // Give the server a chance to return an error
    process.exit();
  });
});
~~~~

