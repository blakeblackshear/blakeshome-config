var fs = require('fs');
var token_string = fs.readFileSync('/etc/nginx/tokens.json');
var tokens = JSON.parse(token_string);

function get_token(r) {
    var email = r.variables["email"];
    r.headersOut['Content-Type'] = 'text/plain';
    if (email == '') {
        r.return(500, "No email found");
    }
    var token = tokens[email];
    if (token == undefined) {
        r.return(500, "No token found");
    }
    return r.return(200, token);
}
