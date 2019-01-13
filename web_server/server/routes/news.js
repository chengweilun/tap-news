var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/', function(req, res, next) {
  news = [{
      "source": "Google News",
      "author": "Christal Hayes",
      "title": "Julian Castro, a Texas Democrat and former Obama cabinet member, announces 2020 bid for president",
      "description": "Julian Castro, a former Obama cabinet member and San Antonio mayor, officially threw his hat in the ring on Saturday and announced he would run for president.",
      "url": "https://www.usatoday.com/story/news/politics/2019/01/12/julian-castro-obama-cabinet-member-announces-bid-2020-president/2484024002/?utm_source=google&utm_medium=amp&utm_campaign=speakable",
      "urlToImage": "https://www.gannett-cdn.com/-mm-/b2b05a4ab25f4fca0316459e1c7404c537a89702/c=0-0-1365-768/local/-/media/2018/07/30/USATODAY/usatsports/247WallSt.com-247WS-482546-imageforentry690.jpg?width=3200&height=1680&fit=crop",
      "publishedAt": "2019-01-12T17:53:00+00:00",
      "content": "Hear remarks that former U.S. Secretary of Housing and Urban Development Julián Castro had at a house party in Iowa on Jan. 7, 2018. Joseph Cress, Iowa City Press-Citizen WASHINGTON Julian Castro, a former Obama cabinet member and San Antonio mayor, officiall… [+7182 chars]"
  },
      {
          "source": "Google News",
          "author": "Elizabeth Chuck",
          "title": "When Jayme Closs escaped, 'I know exactly how she felt': Past kidnap survivors speak out",
          "description": "Past kidnap victims Elizabeth Smart and Michelle Knight told NBC News they are overjoyed that the Wisconsin teen was found safe, and recalled their own recovery after escaping captivity.",
          "url": "https://www.nbcnews.com/news/us-news/when-jayme-closs-escaped-i-know-exactly-how-she-felt-n957866",
          "urlToImage": "https://media3.s-nbcnews.com/j/newscms/2019_02/2712856/190111-elizabeth-smart-ew-216p_aa5897035b7777e4a57c6d3f0a60c146.1200;630;7;70;5.jpg",
          "publishedAt": "2019-01-12T17:28:00+00:00",
          "content": "Breaking News Emails Get breaking news alerts and special reports. The news and stories that matter, delivered weekday mornings. SUBSCRIBE Jan. 12, 2019, 5:28 PM GMT They made headlines for the darkest of reasons, then again for a most improbable one: escapin… [+5723 chars]"
      },
      {
          "source": "Google News",
          "author": "John Bowden",
          "title": "Pompeo: 'Ludicrous' to think Trump is threat to US national security",
          "description": "Secretary of State Mike Pompeo says in an interview set to air Sunday that it is \"ludicrous\" to think that President Trump is a threat to national security.",
          "url": "https://thehill.com/policy/national-security/425042-pompeo-ludicrous-to-think-trump-is-threat-to-us-national-security",
          "urlToImage": "https://thehill.com/sites/default/files/pompeomike_112818sr_lead.jpg",
          "publishedAt": "2019-01-12T16:27:12+00:00",
          "content": "Secretary of State Mike Pompeo Michael (Mike) Richard Pompeo Pompeo says US to host world summit focused on Iran next month The Hill's Morning Report Trump eyes wall money options as shutdown hits 21 days Trump cancels Davos trip over shutdown MORE says in an… [+3294 chars]"
      }];
  res.json(news);
  // res.send('respond with a resource');
});

module.exports = router;
