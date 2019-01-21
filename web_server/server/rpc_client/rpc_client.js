var jayson = require('jayson');
var client = jayson.client.http({
        port: 4040,
        hostname: 'localhost'
});

function getNewsSummariesForUser(user_id,page_num,callback) {
  client.request('getNewsSummariesForUser',[user_id,page_num],function(err,error,response) {
    if (err) throw err;
    console.log(response);
    callback(response);
  })
}

function logNewsClickForUser(user_id, news_id) {
  client.request('logNewsClickForUser', [user_id, news_id], function(err, response) {
    if(err) throw err;
  });
};

module.exports = {
    getNewsSummariesForUser: getNewsSummariesForUser,
    logNewsClickForUser: logNewsClickForUser
};
