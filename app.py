def createDummy(x, n):
    for i in range(n):
        for j in range(n):
            if i > 0 and j > 0 and i < n-1 and j < n-1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))
                x.add_path((i, j), (i, j+1))
            elif i == 0 and j == 0 and n > 1:
                x.add_path((0, 0), (0, 1))
                x.add_path((0, 0), (1, 0))
            elif i == 0 and j == n-1 and n > 1:
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))
            elif i == n-1 and j == 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i, j+1))
            elif i == n-1 and j == n-1 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i, j-1))
            elif i == 0 and j != n-1 and j != 0 and n > 1:
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))
                x.add_path((i, j), (i, j+1))
            elif j == 0 and i != n-1 and i != 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j+1))
            elif i == n-1 and j != n-1 and j != 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i, j-1))
                x.add_path((i, j), (i, j+1))
            elif j == n-1 and i != n-1 and i != 0 and n > 1:
                x.add_path((i, j), (i-1, j))
                x.add_path((i, j), (i+1, j))
                x.add_path((i, j), (i, j-1))


if __name__ == '__main__':
    import time
    from Navigation import Navigation
    from DifferentialDrive import DifferentialDrive
    from datetime import datetime
    navigation = Navigation()
    diffdrive = DifferentialDrive(1)
    t = time.time()
    n = int(input('Enter map size: '))
    createDummy(navigation, n)
    print('Created Map in {}s'.format(time.time()-t))
    navigation.set_position(0, 0, 0)
    print('Set Current Position : {}'.format((0, 0, 0)))
    navigation.set_goal(n-1, n-1, 90)
    print('Set Goal : {}'.format((n-1, n-1, 0)))
    t = time.time()
    navigation.calculate_shortest_path()
    print('Calculated path in {}s'.format(time.time()-t))
    print(navigation.path)
    t = time.time()
    print('Delete node : {}, {}, {}, {}'.format((0, n//4), (n*3//4, n//4), (n//4, 0), (n*3//4, n*3//4)))
    navigation.del_node((0, n//4))
    navigation.del_node((n*3//4, n//4))
    navigation.del_node((n//4, 0))
    navigation.del_node((n*3//4, n*3//4))
    print('Modified Map in {}s'.format(time.time()-t))
    t = time.time()
    navigation.calculate_shortest_path()
    print('Calculated path in {}s'.format(time.time()-t))
    print(navigation.path)
    t = time.time()
    diffdrive.create_robot_motion(navigation)
    print('Calculated robot motion in {}s'.format(time.time()-t))
    print(diffdrive.robot_motion, end='\n-----------------------------\n')
    current_position = (0, 0, 90)
    while True:
        if diffdrive.turn_timer != 0:
            for i in range(10):
                motor_speed = diffdrive.get_motor_speed(current_position[0], current_position[1], current_position[2],
                                                        datetime.now().timestamp())
                print(motor_speed)
                time.sleep(diffdrive.turn_period/10)
            diffdrive.turn_timer = 0
            continue
        else:
            current_position = diffdrive.robot_motion[0]
        motor_speed = diffdrive.get_motor_speed(current_position[0], current_position[1], current_position[2],
                                                datetime.now().timestamp())
        if motor_speed != (0, 0):
            print(motor_speed)
        else:
            break