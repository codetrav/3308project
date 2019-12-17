/***********************
 
  Load Components!

  Express      - A Node.js Framework
  Body-Parser  - A tool to help use parse the data in a post request
  Pug          - A view engine for dynamically rendering HTML pages
  Pg-Promise   - A database tool to help use connect to our PostgreSQL database

***********************/

const express = require('express'); // Add the express framework has been added
var app = express();
const util = require('util');
const bodyParser = require('body-parser'); // Add the body-parser tool has been added
app.use(bodyParser.json({ type: 'application/json' }));              // Add support for JSON encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // Add support for URL encoded bodies
app.use(function (req, res, next) {
    console.log("Request Body " + util.inspect(req.body))
    next()
})

//Create Database Connection
const pgp = require('pg-promise')();
//import sessions
pgp.pg.types.setTypeParser(1114, str => str);

var session = require('client-sessions');
const fetch = require('node-fetch');

const adminSecret = process.env.ADMIN_SECRET;
const hgeEndpoint = process.env.HGE_ENDPOINT;
/**********************
  
  Database Connection information

  host: This defines the ip address of the server hosting our database.  We'll be using localhost and run our database on our local machine (i.e. can't be access via the Internet)
  port: This defines what port we can expect to communicate to our database.  We'll use 5432 to talk with PostgreSQL
  database: This is the name of our specific database.  From our previous lab, we created the football_db database, which holds our football data tables
  user: This should be left as postgres, the default user account created when PostgreSQL was installed
  password: This the password for accessing the database.  You'll need to set a password USING THE PSQL TERMINAL THIS IS NOT A PASSWORD FOR POSTGRES USER ACCOUNT IN LINUX!

**********************/
//session stuff
app.use(session({
    cookieName: 'session',
    secret: 'sddasd5asdasd9',
    duration: 30 * 60 * 1000,
    activeDuration: 5 * 60 * 1000,
}));

//postgres stuff
var dbConfig = process.env.DATABASE_URL;
if (dbConfig == undefined) {
    dbConfig = {
        host: 'localhost',
        port: 5432,
        database: 'car',
        user: 'demo',
        password: 'Sweden77'
    };
}
var db = pgp(dbConfig);
// set the view engine to ejs
app.set('view engine', 'pug');
app.use(express.static(__dirname + '/')); // This line is necessary for us to use relative paths and access our resources directory
console.log('3000 is the magic port');
//helper sql functions
app.get('/', function (req, res) {
    console.log("Booting into home");
    res.redirect('/home');
});
var port = process.env.PORT
console.log(port)
var WebSocketServer = require("ws").Server
const request = require('request')

var http = require('http');
var server = http.createServer(app)
server.listen(port)

console.log("http server listening on %d", port)

var wsServer = new WebSocketServer({ server: server })
console.log("websocket server created")

// WebSocket server
wsServer.on('connection', ws => {
    console.log("Connected")
    ws.on('message', message => {
        console.log(`Received message => ${message}`)
    })
});

//before car is chosen, user may be logged in or out
app.get('/home', function (req, res) {
    //if user is logged in show car list
    if (req.session.user) {
        var car_data = 'SELECT * FROM cars WHERE owner = ' + req.session.user.id
        db.task('get-everything', task => {
            return task.batch([
                task.any(car_data)
            ]);
        })
            .then(data => {
                res.render('pages/home', {
                    my_title: "SmartOBD Demo Data",
                    car_name: "Choose Car:",
                    user_name: req.session.user.username,
                    car_list: data[0]
                })
            })
            .catch(error => {
                //show error and render
                console.log(error);
                res.render('pages/home', {
                    my_title: "data error",
                    car_name: "Choose Car:",
                    user_name: '',
                    car_list: ''
                })
            });
    }
    //if user is not logged in render empty info
    else {
        res.render('pages/home', {
            my_title: "SmartOBD Demo Data",
            car_name: "Choose Car:",
            user_name: '',
            car_list: ''
        })
    }
});
//home after car is chosen, user is logged in
app.post('/home', function (req, res) {
    var num = req.body.car_choice - 1
    console.log(num);
    var car_data = 'SELECT * FROM car' + num + ' ORDER BY time DESC';
    if (req.session.user) {
        db.task('get-everything', task => {
            return task.batch([
                task.any(car_data)
            ]);
        })
            .then(data => {
                console.log(data[0][0]);
                res.render('pages/home', {
                    my_title: "SmartOBD Demo Data",
                    car_name: "Choose Car:",
                    user_name: req.session.user.username,
                    car_list: '',
                    car_data: data[0][0],
                    car_num: num
                })
            })
            .catch(error => {
                // display error message in case an error
                console.log(error);
                res.render('pages/home', {
                    car_name: "Choose Car:",
                    my_title: "data error",
                    user_name: '',
                    car_list: '',
                    car_data: ''
                })
            });
    }
    else {
        res.render('pages/home', {

            my_title: "SmartOBD Demo Data",
            car_name: "Choose Car:",
            user_name: '',
            car_list: '',
            car_data: ''

        })
    }
});
app.get('/login', function (req, res) {
    res.render('pages/login', {
        my_title: "Login",
    })
});
app.post('/login', function (req, res) {
    var inputname = req.body.uname;
    user_validate = 'SELECT * FROM users where username = ' + "'" + inputname + "'";
    db.task('get-everything', task => {
        return task.batch([
            task.any(user_validate),
        ]);
    })
        .then(data => {
            if (data[0][0].username != inputname) {
                res.redirect('/login');
                console.log('whoops');
            }
            else {
                var cor = data[0][0].password;
                if (req.body.pword === cor) {
                    // sets a cookie with the user's info
                    req.session.user = data[0][0];
                    res.redirect('/home');
                }
                else {
                    res.redirect('/login')
                }

            }
        })
        .catch(() => {
            // display error message in case an error
            res.render('pages/login', {
                title: 'Try login again',
            })
        });

});

app.get('/new_user', function (req, res) {
    res.render('pages/new_user', {
        my_title: "New User",
    })
});

app.get('/logout', function (req, res) {
    req.session.reset();
    res.redirect('/home');
});

app.post('/new_user', function (req, res) {
    var first = req.body.fname;
    var last = req.body.lname;
    var email = req.body.email;
    var pass = req.body.password;
    var username = req.body.username_input;
    var insert_statement = "INSERT INTO users(username,password,firstname,lastname,email) VALUES('" + username + "','" +
        pass + "','" + first + "','" + last + "','" + email + "')";
    db.task('get-everything', task => {
        return task.batch([
            task.any(insert_statement),
        ]);
    })
        .then(
            res.redirect('/login')
        )
        .catch(() => {
            // display error message in case an error
            res.render('pages/home', {
                title: 'Home Page',
                car_name: "Choose Car:",
                data: '',
                color: '',
                color_msg: ''
            })
        });
});
//before car or times are chosen, user may be logged in or out
app.get('/full_log', function (req, res) {
    if (req.session.user != undefined) {
        var car_list = 'SELECT id , model FROM cars WHERE owner = ' + req.session.user.id;
        db.task('get-everything', task => {
            return task.batch([
                task.any(car_list)
            ]);
        })
            .then(data => {
                res.render('pages/full_log', {
                    my_title: "SmartOBD Demo Data",
                    user_name: req.session.user.username,
                    car_list: data[0],
                    time_list: ''
                })
            })
            .catch(error => {
                //show error and render
                console.log(error);
                res.render('pages/home', {
                    my_title: "data error",
                    car_name: "Choose Car:",
                    user_name: '',
                    car_list: '',
                    time_list: ''
                })
            });
    }
    //if user is not logged in render empty info
    else {
        res.render('pages/full_log', {
            my_title: "SmartOBD Demo Data",
            user_name: '',
            car_list: ''
        })
    }
});
app.get('/full_log/got', function (req, res) {
    var car_data = 'SELECT * FROM car' + (req.query.car_choice - 1) + ' WHERE time=' + '\'' + req.query.time_choice + '\'';
    var car_list = 'SELECT id , model FROM cars WHERE owner = ' + req.session.user.id;
    console.log(req.query.time_choice);
    db.task('get-everything', task => {
        return task.batch([
            task.any(car_data),
            task.any(car_list)
        ]);
    })
        .then(data => {
            console.log("Car Data " + util.inspect(data, { depth: null }));

            res.render('pages/full_log', {
                my_title: "SmartOBD Demo Data",
                user_name: req.session.user.username,
                time_list: '',
                car_list: '',
                car_data: data[0][0],
                car_list_2: data[1],
                car_num: req.query.car_choice - 1
            })
        })
        .catch(error => {
            //show error and render
            console.log(error);
            res.render('pages/home', {
                my_title: "data error",
                car_name: "Choose Car:",
                user_name: '',
                car_list: ''
            })
        });
});
app.get('/full_log/findTime', function (req, res) {
    var choice = req.query.car_choice;
    var array = JSON.parse(choice);
    var time_list = 'SELECT DISTINCT time FROM car' + (array[1] - 1);
    var car_list = 'SELECT * FROM cars WHERE id = ' + (array[1]);
    db.task('get-everything', task => {
        return task.batch([
            task.any(time_list),
            task.any(car_list)
        ]);
    })
        .then(data => {
            console.log(util.inspect(data[0]));
            res.render('pages/full_log', {
                my_title: "SmartOBD Demo Data",
                user_name: req.session.user.username,
                time_list: data[0],
                car_data: data[1][0],
                car_num: array[1] - 1
            })

        })
        .catch(error => {
            //show error and render
            console.log(error);
            res.render('pages/home', {
                my_title: "data error",
                car_name: "Choose Car:",
                user_name: '',
                car_list: ''
            })
        });
});
async function renderUserPage(vals, res, req) {
    console.log("Array Indexing " + util.inspect(vals))
    if (vals == null) {
        vals = { time: "", 'SPEED KMPH': '', 'FUEL LEVEL': '', RPM: '', MAF: '', voltage: '', 'Coolant Temp': '' }
    }
    return res.render('pages/live', {
        title: "SmartOBD Demo Data",
        port: port
    });
};
app.get('/live', function (req, res) {
    renderUserPage(null, res, req);
    request.post('https://wiwa-hasura.herokuapp.com/v1/graphql', {

    }, (error, res, body) => {
        if (error) {
            console.error(error)
            return
        }
        console.log(`statusCode: ${res.statusCode}`)
        console.log(body)
    })
});

app.post('/live', function (req, res) {
    values = req.body.event.data.new;
    res.statusCode = 202;
    wsServer.clients.forEach((client) => {
        client.send(JSON.stringify(values));
    });
    renderUserPage(values, res, req);
});

app.get('/downloads', function (req, res) {

    res.render('pages/downloads', {
        my_title: "SmartOBD Demo Data"
    })
});
app.get('/export', function (req, res) {

    var car_data = 'SELECT * FROM users;'
    db.task('get-everything', task => {
        return task.batch([
            task.any(car_data)
        ]);
    })
        .then(() => {
            res.render('pages/export', {
                my_title: "SmartOBD Demo Data",
                user_name: req.session.user.username
            })
        })
        .catch(error => {
            // display error message in case an error
            console.log(error);
            res.render('pages/export', {
                my_title: "data error",
                user_name: ''
            })
        });
});
app.get('/:file(*)', function (req, res) {
    var file = req.params.file
        , path = __dirname + '/views/pages/downloads/' + file;

    res.download(path);
    res.redirect('/downloads')
});
app.get('/', function (req, res) {
    res.redirect('/home');
});

