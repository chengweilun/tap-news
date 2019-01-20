from cloudAMQP_client import cloudAMQPClient

CLOUDAMQP_URL = "amqp://avqwoxul:DnLJdgb71xYI_2bNIC5myl9-6NF-Hsop@hornet.rmq.cloudamqp.com/avqwoxul"

TEST_QUEUE_NAME = 'test'

def test_basic():
    client = cloudAMQPClient(CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test':'demo'}
    client.sendMessage(sentMsg)
    client.sleep(10)
    receiveMsg = client.getMessage()
    assert sentMsg == receiveMsg
    print "test_basic passed"

if __name__ =="__main__":
    test_basic()
