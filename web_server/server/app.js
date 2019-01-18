var bodyParser = require('body-parser');
var cors = require('cors');
var createError = require('http-errors');
var express = require('express');
var path = require('path');
var passport = require('passport');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use(bodyParser.json());
//TODO: remove this after development is done
app.use(cors());


var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

const authCheckMiddleWare = require('./middleware/auth_checker');
app.use('/news', authCheckMiddleWare);

const authChecker = require('./middleware/auth_checker');
app.use('/news', authChecker);

app.all('*',function (req,res,next) {
    res.header("Access-Control-Allow-Origin","*");
    res.header("Access-Control-Allow-Header","X-Requested-With");
    next();
});
app.use(express.static(path.join(__dirname, '../client/build/')));
app.use('static',express.static(path.join(__dirname,'../client/build/static')));
app.use('/', index);
// app.use('/users', usersRouter);
app.use('/news',news);
app.use('/auth',auth);



// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
