var http = require('http'),
    url = require('url'),
    qs = require('querystring');
// MongoDB tools
var Db = require('mongodb').Db;
var Connection = require('mongodb').Connection;
var Server = require('mongodb').Server;
var BSON = require('mongodb').BSON;
var ObjectID = require('mongodb').ObjectID;

DataProvider = function(host, port) {
    this.db= new Db('perftest', new Server(host, port, {auto_reconnect: true}, {}));
    this.db.open(function(){});
};


DataProvider.prototype.getCollection= function(callback) {
  this.db.collection('messages', function(error, coll) {
    if( error )
        callback(error);
    else
        callback(null, coll);
  });
};

DataProvider.prototype.findById = function(id, callback) {
    this.getCollection(function(error, coll) {
        if( error )
            callback(error)
        else {
            coll.findOne({_id: id}, function(error, result) {
              if( error )
                callback(error)
              else
                callback(null, result)
            });
      }
    });
};

var dataProvider = new DataProvider('localhost', 27017);

var paths = {
    '__default__': function (req, res) {
        id = req.url.pathname.split('/').join('');

        dataProvider.findById(parseInt(id), function(error, msg) {
            // console.log(msg);
            res.writeHead(200, {'Content-Type': 'text/plain'});
            res.end('200 OK');
        });
    }
};

var app = http.createServer(function (req, res) {
  //URI format - scheme://domain:port/path?query_string#fragment_id
  // console.log('-> ' + req.url);
  req.setEncoding('utf8');
  req.body = '';
  req.url = url.parse(qs.unescape(req.url));
  // console.log(req.url);

  if (req.method === 'OPTIONS') {
      var headers = {};
      headers["Access-Control-Allow-Origin"] = "*";
      headers["Access-Control-Allow-Methods"] = "POST, GET, PUT, DELETE, OPTIONS";
      headers["Access-Control-Allow-Credentials"] = false;
      headers["Access-Control-Max-Age"] = '86400'; // 24 hours
      headers["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept";
      res.writeHead(200, headers);
      res.end();
  } else {
      var f = paths[req.url.pathname] || paths['__default__'];
      f.call(this, req, res);
  }
});

module.exports = app;

if (!module.parent) {
  app.listen(8888);
  console.log("Server listening on port %d", app.address().port);
}
