/***********************
 
  Load Components!

  Express      - A Node.js Framework
  Body-Parser  - A tool to help use parse the data in a post request
  Pug          - A view engine for dynamically rendering HTML pages
  Pg-Promise   - A database tool to help use connect to our PostgreSQL database

***********************/

const express = require('express'); // Add the express framework has been added
let app = express();

const bodyParser = require('body-parser'); // Add the body-parser tool has been added
app.use(bodyParser.json());              // Add support for JSON encoded bodies
app.use(bodyParser.urlencoded({ extended: true })); // Add support for URL encoded bodies

const pug = require('pug'); // Add the 'pug' view engine

//Create Database Connection
const pgp = require('pg-promise')();
//import sessions
var session = require('client-sessions');

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
const dbConfig = {
	host: 'localhost',
	port: 5432,
	database: 'car',
	user: 'demo',
    password: 'Sweden77'
};

let db = pgp(dbConfig);

// set the view engine to ejs
app.set('view engine', 'pug');
app.use(express.static(__dirname + '/')); // This line is necessary for us to use relative paths and access our resources directory
//helper sql functions


//before car is chosen, user may be logged in or out
app.get('/home', function(req, res) {
//if user is logged in show car list
if(req.session.user){
var car_data = 'SELECT * FROM cars WHERE owner = ' + req.session.user.id
db.task('get-everything', task => {
    return task.batch([
        task.any(car_data)
    ]);
})
.then(data => {
  res.render('pages/home',{
      my_title: "SmartOBD Demo Data",
      user_name: req.session.user.username,
	  car_list: data[0]
    })
})
.catch(error => {
    //show error and render
        console.log(error);
        res.render('pages/home',{
      my_title: "data error",
      user_name: '',
	  car_list: ''
    })
});
}
//if user is not logged in render empty info
else{
	res.render('pages/home',{
      my_title: "SmartOBD Demo Data",
      user_name: '',
	  car_list: ''
    })
}
});
//home after car is chosen, user is logged in
app.post('/home', function(req, res) {
var num = req.body.car_choice
var car_list = 'SELECT * FROM cars WHERE owner = ' + req.session.user.id
var car_data = 'SELECT * FROM car' + num + ' ORDER BY time'
if(req.session.user){
	db.task('get-everything', task => {
    return task.batch([
        task.any(car_list),
        task.any(car_data)
    ]);
})
.then(data => {
  res.render('pages/home',{
	  
      my_title: "SmartOBD Demo Data",
      user_name: req.session.user.username,
	  car_list: data[0],
	  car_data: data[1][0]
	  
    })
})
.catch(error => {
    // display error message in case an error
        console.log(error);
        res.render('pages/home',{
      my_title: "data error",
      user_name: '',
	  car_list: '',
	  car_data: ''
    })
});
}
else{
	  res.render('pages/home',{
	  
      my_title: "SmartOBD Demo Data",
      user_name: '',
	  car_list: '',
	  car_data: ''
	  
    })
}
});
app.get('/login', function(req, res) {
	res.render('pages/login',{
		my_title: "Login",
    })
});
app.post('/login', function(req, res) {
    var inputname = req.body.uname;
	var inputpass = req.body.pword;
    user_validate = 'SELECT * FROM users where username = '+ "'"+inputname+"'";
    db.task('get-everything', task => {
        return task.batch([
            task.any(user_validate),
    ]);
})
.then(data => {
    if(data[0][0].username != inputname){
		res.redirect('/login');
		console.log('whoops');
	}
	else{
		var cor = data[0][0].password;
		if (req.body.pword === cor) {
        // sets a cookie with the user's info
        req.session.user = data[0][0];
        res.redirect('/home');
		}
		else{
			res.redirect('/login')
		}
  
    }
})    
.catch(error => {
        // display error message in case an error
            res.render('pages/login', {
                title: 'Try login again',
            })
    });

  });

app.get('/new_user', function(req, res) {
	res.render('pages/new_user',{
		my_title: "New User",
    })
});

app.get('/logout', function(req, res) {
  req.session.reset();
  res.redirect('/home');
});

app.post('/new_user', function(req, res) {
  var first = req.body.fname;
  var last = req.body.lname;
  var email = req.body.email;
  var pass = req.body.password;
  var username = req.body.username_input;
  var insert_statement = "INSERT INTO users(username,password,firstname,lastname,email) VALUES('" + username + "','" +
              pass + "','" + first + "','"+ last +"','"+ email +"')";
  db.task('get-everything', task => {
        return task.batch([
            task.any(insert_statement),
        ]);
    })
    .then(
      res.redirect('/login')
    )
    .catch(error => {
        // display error message in case an error
            res.render('pages/home', {
                title: 'Home Page',
                data: '',
                color: '',
                color_msg: ''
            })
    });
});
//before car or times are chosen, user may be logged in or out
app.get('/full_log', function(req, res) {


var car_list = 'SELECT * FROM cars WHERE owner = ' + req.session.user.id;
var time_list = 'SELECT time FROM car'+ req.query.car_choice + ' WHERE owner = ' + req.session.user.id;
console.log(time_list);
db.task(t => {
    return t.oneOrNone(car_list)
        .then(cars => {
            console.log(cars[0]);
            if(typeof cars[0] !== 'undefined') {

                return t.any(time_list);
            }
            return [];
        });
})
    .then(events => {
      res.render('pages/full_log',{
	  
      my_title: "SmartOBD Demo Data",
      user_name: req.session.user.username,
	  car_list: cars[0],
	  time_list: events[0]
	  
    })
    })
    .catch(error => {
      if(events)
      res.render('pages/full_log',{
      my_title: "SmartOBD Demo Data",
      user_name: req.session.user.username,
	  car_list: '',
	  time_list: ''
	  
    })
	console.log("haha");
    });
});
app.get('/live', function(req, res) {

var car_data = 'SELECT * FROM users;'
db.task('get-everything', task => {
    return task.batch([
        task.any(car_data)
    ]);
})
.then(data => {
  res.render('pages/live',{
      my_title: "SmartOBD Demo Data",
      user_name: req.session.user.username
    })
})
.catch(error => {
    // display error message in case an error
        console.log(error);
        res.render('pages/live',{
      my_title: "data error",
      user_name: ''
    })
});
});


app.get('/downloads', function(req, res) {

var car_data = 'SELECT * FROM users;'
db.task('get-everything', task => {
    return task.batch([
        task.any(car_data)
    ]);
})
.then(data => {
  res.render('pages/downloads',{
      my_title: "downloads",
      user_name: req.session.user.username
    })
})
.catch(error => {
    // display error message in case an error
        console.log(error);
        res.render('pages/downloads',{
      my_title: "data error",
      user_name: ''
    })
});
});



app.get('/export', function(req, res) {

var car_data = 'SELECT * FROM users;'
db.task('get-everything', task => {
    return task.batch([
        task.any(car_data)
    ]);
})
.then(data => {
  res.render('pages/export',{
      my_title: "SmartOBD Demo Data",
      user_name: req.session.user.username
    })
})
.catch(error => {
    // display error message in case an error
        console.log(error);
        res.render('pages/export',{
      my_title: "data error",
      user_name: ''
    })
});
});

app.listen(3000);
console.log('3000 is the magic port');
