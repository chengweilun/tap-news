import cnn_news_scrapers as scraper

EXPECTED_NEWS = "President Donald Trump plans to offer Democrats another proposal to end the shutdown when he addresses the nation from the White House on Saturday afternoon -- what officials are describing as his third offer to end the shutdown, according to a senior administration official."
CNN_NEWS_URL = "https://www.cnn.com/2019/01/18/politics/trump-saturday-speech-shutdown/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    print(news)
    assert EXPECTED_NEWS in news
    print('test_basic passed!')

if __name__ == "__main__":
    test_basic()