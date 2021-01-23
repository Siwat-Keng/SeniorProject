from rospy import init_node, Subscriber, Publisher, Rate, is_shutdown
from os import getenv
from dotenv import load_dotenv

load_dotenv()

NODE_NAME = getenv('NODE_NAME')

SUBSCRIBE_TOPIC = getenv('SUBSCRIBE_TOPIC')
THE_TYPE_OF_THE_MESSAGE_SUBSCRIBE_TOPIC = eval(
    getenv('THE_TYPE_OF_THE_MESSAGE_SUBSCRIBE_TOPIC'))

PUBLISH_TOPIC = getenv('PUBLISH_TOPIC')
THE_TYPE_OF_THE_MESSAGE_PUBLISH_TOPIC = eval(
    getenv('THE_TYPE_OF_THE_MESSAGE_PUBLISH_TOPIC'))
QUEUE_SIZE = int(getenv('QUEUE_SIZE'))

ROS_RATE = int(getenv('ROS_RATE'))


def subscribe_callback(msg):
    # TODO
    return msg


if __name__ == '__main__':
    init_node(NODE_NAME)

    subscriber = Subscriber(
        SUBSCRIBE_TOPIC, THE_TYPE_OF_THE_MESSAGE_SUBSCRIBE_TOPIC, subscribe_callback)
    publisher = Publisher(
        PUBLISH_TOPIC, THE_TYPE_OF_THE_MESSAGE_PUBLISH_TOPIC, queue_size=QUEUE_SIZE)
    rate = Rate(ROS_RATE)

    while not is_shutdown():
        # TODO
        rate.sleep()
