from rospy import init_node, Subscriber, Publisher, Rate, is_shutdown
from sensor_msgs import String

def subscribe_callback(msg):
    # TODO
    return msg


if __name__ == '__main__':
    init_node('planning')

    subscriber = Subscriber(
        'robot_state', String, subscribe_callback)
    publisher = Publisher(
        'robot_state', String, queue_size=1)
    rate = Rate(ROS_RATE)

    while not is_shutdown():
        # TODO
        rate.sleep()
