var http = require("http");

var delayed_response = function(request, response) {
    var respond = function() {
        response.writeHead(200, {"Content-Type": "text/html"});
        response.write("<html><body>Ok</body></html>");
        response.end();
    };
    setTimeout(respond, 30000);
};
http.createServer(delayed_response).listen(8080);